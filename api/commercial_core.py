from pathlib import Path

import pandas as pd

from api.access import read_usage_records, summarize_usage_by_endpoint
from security.limits import build_limit_status


ACCOUNTS_FILE = Path("data/customer_accounts.csv")
PRICING_FILE = Path("data/plan_pricing.csv")


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def read_plan_pricing():
    pricing = {}
    for row in read_records(PRICING_FILE):
        plan = row.get("plan")
        if not plan:
            continue
        pricing[str(plan)] = float(row.get("monthly_price_usd", 0))
    return pricing


def usage_for_key(api_key):
    return [
        row for row in read_usage_records()
        if row.get("api_key") == api_key
    ]


def build_account_snapshot(account, pricing):
    api_key = account.get("api_key")
    plan = account.get("plan")
    usage = usage_for_key(api_key)
    limits = build_limit_status(plan, usage)
    monthly_price = pricing.get(plan, 0)
    daily_limit = limits.get("limits", {}).get("requests_per_day", 0)
    monthly_limit = limits.get("limits", {}).get("requests_per_month", 0)
    daily_calls = limits.get("daily_calls", 0)
    monthly_calls = limits.get("monthly_calls", 0)
    daily_utilization = (daily_calls / daily_limit) if daily_limit else 0
    monthly_utilization = (monthly_calls / monthly_limit) if monthly_limit else 0

    upgrade_signal = "none"
    if plan == "free" and monthly_calls > 0:
        upgrade_signal = "convert_to_pro"
    elif plan == "pro" and monthly_utilization >= 0.8:
        upgrade_signal = "expand_to_enterprise"
    elif plan == "enterprise" and monthly_calls > 0:
        upgrade_signal = "retain_and_expand"

    return {
        "account_id": account.get("account_id"),
        "customer_name": account.get("customer_name"),
        "api_key": api_key,
        "plan": plan,
        "status": account.get("status"),
        "monthly_price_usd": monthly_price,
        "usage": {
            "total_calls": len(usage),
            "by_endpoint": summarize_usage_by_endpoint(usage),
            "recent": usage[-10:],
        },
        "limits": limits,
        "utilization": {
            "daily": round(daily_utilization, 4),
            "monthly": round(monthly_utilization, 4),
        },
        "upgrade_signal": upgrade_signal,
    }


def build_commercial_snapshot():
    accounts = read_records(ACCOUNTS_FILE)
    pricing = read_plan_pricing()
    account_snapshots = [
        build_account_snapshot(account, pricing)
        for account in accounts
        if account.get("status") == "active"
    ]

    mrr = sum(account["monthly_price_usd"] for account in account_snapshots)
    usage_total = sum(account["usage"]["total_calls"] for account in account_snapshots)
    accounts_by_plan = {}

    for account in account_snapshots:
        plan = account.get("plan", "unknown")
        accounts_by_plan[plan] = accounts_by_plan.get(plan, 0) + 1

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "commercial_snapshot",
        "summary": {
            "active_accounts": len(account_snapshots),
            "mrr_usd": mrr,
            "annual_run_rate_usd": mrr * 12,
            "usage_total": usage_total,
            "accounts_by_plan": accounts_by_plan,
        },
        "accounts": account_snapshots,
    }


def make_sales_opportunity(account):
    plan = account.get("plan")
    signal = account.get("upgrade_signal")
    usage = account.get("usage", {})
    utilization = account.get("utilization", {})

    if signal == "convert_to_pro":
        return {
            "account_id": account.get("account_id"),
            "customer_name": account.get("customer_name"),
            "current_plan": plan,
            "opportunity_type": "conversion",
            "priority": "medium",
            "recommended_action": "Offer Pro trial or buyer call",
            "rationale": "The free account has active usage and can be converted into a paid Pro subscription.",
            "estimated_mrr_lift_usd": 299,
            "evidence": {
                "total_calls": usage.get("total_calls", 0),
                "monthly_utilization": utilization.get("monthly", 0),
            },
        }

    if signal == "expand_to_enterprise":
        return {
            "account_id": account.get("account_id"),
            "customer_name": account.get("customer_name"),
            "current_plan": plan,
            "opportunity_type": "expansion",
            "priority": "high",
            "recommended_action": "Start Enterprise expansion conversation",
            "rationale": "The Pro account is approaching plan capacity and may need enterprise limits or reporting.",
            "estimated_mrr_lift_usd": 2201,
            "evidence": {
                "total_calls": usage.get("total_calls", 0),
                "monthly_utilization": utilization.get("monthly", 0),
            },
        }

    if signal == "retain_and_expand":
        return {
            "account_id": account.get("account_id"),
            "customer_name": account.get("customer_name"),
            "current_plan": plan,
            "opportunity_type": "retention",
            "priority": "medium",
            "recommended_action": "Schedule quarterly business review",
            "rationale": "The enterprise account is active and should be retained through reporting and expansion discovery.",
            "estimated_mrr_lift_usd": 0,
            "evidence": {
                "total_calls": usage.get("total_calls", 0),
                "monthly_utilization": utilization.get("monthly", 0),
            },
        }

    return None


def build_sales_pipeline():
    commercial = build_commercial_snapshot()
    opportunities = [
        opportunity for opportunity in (
            make_sales_opportunity(account)
            for account in commercial["accounts"]
        )
        if opportunity is not None
    ]

    priority_rank = {"high": 0, "medium": 1, "low": 2}
    opportunities = sorted(
        opportunities,
        key=lambda item: (
            priority_rank.get(item.get("priority"), 9),
            -item.get("estimated_mrr_lift_usd", 0),
        ),
    )

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "sales_pipeline",
        "summary": {
            "opportunity_count": len(opportunities),
            "estimated_mrr_lift_usd": sum(
                item["estimated_mrr_lift_usd"] for item in opportunities
            ),
            "high_priority": len([
                item for item in opportunities
                if item.get("priority") == "high"
            ]),
        },
        "opportunities": opportunities,
    }


def build_customer_admin_snapshot():
    accounts = read_records(ACCOUNTS_FILE)
    pricing = read_plan_pricing()
    account_snapshots = [
        build_account_snapshot(account, pricing)
        for account in accounts
    ]

    status_counts = {}
    plan_counts = {}

    for account in account_snapshots:
        status = account.get("status", "unknown")
        plan = account.get("plan", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        plan_counts[plan] = plan_counts.get(plan, 0) + 1

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "customer_admin_snapshot",
        "summary": {
            "total_accounts": len(account_snapshots),
            "status_counts": status_counts,
            "plan_counts": plan_counts,
            "total_usage": sum(
                account["usage"]["total_calls"] for account in account_snapshots
            ),
        },
        "accounts": account_snapshots,
    }


def score_account_health(account):
    status = account.get("status")
    usage = account.get("usage", {})
    utilization = account.get("utilization", {})
    total_calls = usage.get("total_calls", 0)
    monthly_utilization = utilization.get("monthly", 0)

    score = 100
    reasons = []

    if status != "active":
        score -= 70
        reasons.append("account is not active")

    if total_calls == 0:
        score -= 25
        reasons.append("no tracked usage")

    if monthly_utilization >= 0.9:
        score -= 20
        reasons.append("near monthly limit")
    elif monthly_utilization >= 0.75:
        score -= 10
        reasons.append("high monthly utilization")

    score = max(score, 0)

    if score >= 80:
        health = "healthy"
    elif score >= 50:
        health = "watch"
    else:
        health = "at_risk"

    return {
        "account_id": account.get("account_id"),
        "customer_name": account.get("customer_name"),
        "plan": account.get("plan"),
        "status": account.get("status"),
        "health_score": score,
        "health": health,
        "reasons": reasons or ["usage and status are within expected range"],
        "usage_total": total_calls,
        "monthly_utilization": monthly_utilization,
        "upgrade_signal": account.get("upgrade_signal"),
    }


def build_account_health_snapshot():
    admin = build_customer_admin_snapshot()
    accounts = [
        score_account_health(account)
        for account in admin["accounts"]
    ]
    accounts = sorted(
        accounts,
        key=lambda item: (item["health_score"], -item["usage_total"]),
    )
    health_counts = {}

    for account in accounts:
        health = account["health"]
        health_counts[health] = health_counts.get(health, 0) + 1

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "account_health",
        "summary": {
            "account_count": len(accounts),
            "health_counts": health_counts,
            "at_risk": health_counts.get("at_risk", 0),
            "watch": health_counts.get("watch", 0),
        },
        "accounts": accounts,
    }
