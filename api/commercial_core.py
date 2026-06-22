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
