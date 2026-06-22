from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def read_latest(path):
    records = read_records(path)
    if not records:
        return {}
    return records[-1]


def read_latest_report(pattern):
    reports = sorted(REPORTS_DIR.glob(pattern))
    if not reports:
        return {
            "status": "missing",
            "file": None,
            "content": ""
        }

    latest = reports[-1]
    return {
        "status": "ok",
        "file": latest.name,
        "content": latest.read_text()
    }


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def make_signal(signal_type, severity, title, message, evidence):
    return {
        "type": signal_type,
        "severity": severity,
        "title": title,
        "message": message,
        "evidence": evidence
    }


def build_market_signals():
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    risk = read_latest(DATA_DIR / "terminal_risk_score.csv")
    trend = read_latest(DATA_DIR / "gpu_price_trend_signal.csv")
    cheapest = read_records(DATA_DIR / "live_gpu_cheapest.csv")
    expensive = read_records(DATA_DIR / "live_gpu_most_expensive.csv")
    scarcity = read_records(DATA_DIR / "scarcity_watchlist.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")

    signals = []
    risk_score = as_float(risk.get("terminal_risk_score"))
    price_trend = str(trend.get("gpu_price_trend_signal", terminal.get("gpu_price_trend", "unknown")))
    change_pct = as_float(trend.get("change_pct"))

    if risk_score >= 80:
        signals.append(make_signal(
            "risk",
            "high",
            "Infrastructure risk is elevated",
            "Risk is high enough that buyers should monitor capacity and provider reliability before committing spend.",
            {"terminal_risk_score": risk_score}
        ))
    elif risk_score >= 60:
        signals.append(make_signal(
            "risk",
            "medium",
            "Risk is in watch mode",
            "The market is not calm, but current conditions do not require immediate escalation.",
            {"terminal_risk_score": risk_score}
        ))
    else:
        signals.append(make_signal(
            "risk",
            "low",
            "Risk is contained",
            "Current infrastructure risk is within the lower operating range.",
            {"terminal_risk_score": risk_score}
        ))

    if "down" in price_trend or change_pct <= -5:
        signals.append(make_signal(
            "opportunity",
            "medium",
            "GPU price pressure is easing",
            "Recent price movement may create a buying window for flexible workloads.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))
    elif "up" in price_trend or change_pct >= 5:
        signals.append(make_signal(
            "cost",
            "high",
            "GPU price pressure is rising",
            "Rising pricing pressure may increase short-term infrastructure costs.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))
    else:
        signals.append(make_signal(
            "market",
            "low",
            "GPU pricing is stable",
            "Pricing is not showing a strong directional move in the latest observation window.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))

    if cheapest:
        best = cheapest[0]
        signals.append(make_signal(
            "buying_signal",
            "low",
            f"Cheapest tracked GPU: {best.get('gpu', 'unknown')}",
            "This GPU currently offers the lowest average tracked price.",
            {
                "gpu": best.get("gpu"),
                "avg_price": best.get("avg_price"),
                "min_price": best.get("min_price"),
                "offers": best.get("offers")
            }
        ))

    if expensive:
        top = expensive[0]
        signals.append(make_signal(
            "premium_pressure",
            "medium",
            f"Most expensive tracked GPU: {top.get('gpu', 'unknown')}",
            "High average pricing here can indicate frontier demand pressure or limited supply.",
            {
                "gpu": top.get("gpu"),
                "avg_price": top.get("avg_price"),
                "max_price": top.get("max_price"),
                "offers": top.get("offers")
            }
        ))

    scarce_frontier = [
        row for row in scarcity
        if str(row.get("category", "")).lower() == "frontier"
        and str(row.get("scarcity_flag", "")).lower() == "true"
    ]
    if scarce_frontier:
        signals.append(make_signal(
            "scarcity",
            "high",
            "Frontier GPU scarcity detected",
            "One or more frontier GPUs are flagged as scarce and should be watched closely.",
            {
                "gpus": [row.get("gpu") for row in scarce_frontier[:5]],
                "count": len(scarce_frontier)
            }
        ))

    offline = [row.get("provider") for row in provider_health if row.get("status") != "online"]
    if offline:
        signals.append(make_signal(
            "provider_health",
            "medium",
            "Provider health needs attention",
            "At least one tracked provider is not currently reporting as online.",
            {"offline_providers": offline}
        ))

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "signals": signals,
        "signal_count": len(signals)
    }


def build_recommendations():
    signals = build_market_signals()["signals"]
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    provider_comparison = read_records(DATA_DIR / "provider_comparison.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")
    cheapest = read_records(DATA_DIR / "live_gpu_cheapest.csv")
    scarcity = read_records(DATA_DIR / "scarcity_watchlist.csv")

    recommendations = []
    signal_types = {signal.get("type") for signal in signals}
    risk_signal = next((signal for signal in signals if signal.get("type") == "risk"), {})

    online_providers = {
        row.get("provider")
        for row in provider_health
        if row.get("status") == "online"
    }
    ranked_providers = sorted(
        provider_comparison,
        key=lambda row: (
            0 if row.get("provider") in online_providers else 1,
            -as_float(row.get("offers")),
            as_float(row.get("avg_price"), 999999)
        )
    )

    if ranked_providers:
        provider = ranked_providers[0]
        recommendations.append({
            "action": "primary_provider_watch",
            "priority": "high" if risk_signal.get("severity") == "high" else "medium",
            "title": f"Use {provider.get('provider')} as the primary provider benchmark",
            "rationale": "This provider has the strongest current combination of online status and tracked offer depth.",
            "evidence": {
                "provider": provider.get("provider"),
                "offers": provider.get("offers"),
                "gpu_types": provider.get("gpu_types"),
                "avg_price": provider.get("avg_price")
            }
        })

    if "opportunity" in signal_types and cheapest:
        gpu = cheapest[0]
        recommendations.append({
            "action": "evaluate_buy_window",
            "priority": "high",
            "title": f"Evaluate short-term buying window for {gpu.get('gpu')}",
            "rationale": "Price pressure is easing and a low-cost GPU candidate is visible in the live market.",
            "evidence": {
                "gpu": gpu.get("gpu"),
                "avg_price": gpu.get("avg_price"),
                "min_price": gpu.get("min_price"),
                "offers": gpu.get("offers")
            }
        })
    elif cheapest:
        gpu = cheapest[0]
        recommendations.append({
            "action": "track_low_cost_capacity",
            "priority": "medium",
            "title": f"Track low-cost capacity around {gpu.get('gpu')}",
            "rationale": "This is currently the lowest-cost tracked GPU and can anchor budget-sensitive workloads.",
            "evidence": {
                "gpu": gpu.get("gpu"),
                "avg_price": gpu.get("avg_price"),
                "min_price": gpu.get("min_price"),
                "offers": gpu.get("offers")
            }
        })

    scarce_frontier = [
        row for row in scarcity
        if str(row.get("category", "")).lower() == "frontier"
        and str(row.get("scarcity_flag", "")).lower() == "true"
    ]
    if scarce_frontier:
        recommendations.append({
            "action": "protect_frontier_capacity",
            "priority": "high",
            "title": "Protect frontier GPU capacity decisions",
            "rationale": "Frontier GPU scarcity is visible. Avoid relying on a single provider or a single GPU type.",
            "evidence": {
                "scarce_gpus": [row.get("gpu") for row in scarce_frontier[:5]],
                "count": len(scarce_frontier)
            }
        })

    risk_score = as_float(read_latest(DATA_DIR / "terminal_risk_score.csv").get("terminal_risk_score"))
    if risk_score >= 80:
        recommendations.append({
            "action": "escalate_risk_review",
            "priority": "high",
            "title": "Escalate infrastructure risk review",
            "rationale": "Risk is high enough to justify reviewing provider exposure, capacity timing and budget assumptions.",
            "evidence": {"terminal_risk_score": risk_score}
        })
    elif risk_score >= 60:
        recommendations.append({
            "action": "maintain_watch_mode",
            "priority": "medium",
            "title": "Maintain watch mode",
            "rationale": "Risk is elevated but not extreme. Keep monitoring before making irreversible commitments.",
            "evidence": {"terminal_risk_score": risk_score}
        })

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "market_context": {
            "top_provider": terminal.get("top_provider"),
            "gpu_price_trend": terminal.get("gpu_price_trend"),
            "active_alerts": terminal.get("active_alerts")
        },
        "recommendations": recommendations,
        "recommendation_count": len(recommendations)
    }


def build_executive_brief():
    summary = build_terminal_summary()
    signals = build_market_signals()["signals"]
    recommendations = build_recommendations()["recommendations"]

    terminal = summary.get("terminal", {})
    risk = summary.get("risk", {})
    quality = summary.get("quality", {})
    scarcity = summary.get("scarcity", {})
    frontier = summary.get("frontier", {})

    high_priority = [
        item for item in recommendations
        if item.get("priority") == "high"
    ]
    top_recommendations = high_priority[:3] or recommendations[:3]
    top_signals = signals[:5]

    risk_level = risk.get("risk_level", "unknown")
    risk_score = risk.get("terminal_risk_score", "n/a")
    ai_index = terminal.get("ai_infrastructure_index", "n/a")
    gpu_price_index = terminal.get("gpu_price_index", "n/a")
    trend = terminal.get("gpu_price_trend", "unknown")
    top_provider = terminal.get("top_provider", "unknown")

    if risk_level == "high" or as_float(risk_score) >= 75:
        headline = "AI infrastructure risk remains elevated."
        summary_text = (
            "The terminal is showing elevated infrastructure risk, with frontier GPU scarcity "
            "and provider concentration requiring active monitoring."
        )
    elif trend and trend != "stable":
        headline = "GPU market conditions are moving."
        summary_text = (
            "The latest terminal snapshot shows a directional GPU pricing signal. "
            "Buyers should compare provider depth before committing capacity."
        )
    else:
        headline = "AI infrastructure conditions are stable but watchlisted."
        summary_text = (
            "The latest terminal snapshot is stable overall, while selected GPU categories "
            "and provider exposure still deserve monitoring."
        )

    markdown = [
        "# AI-RPCT Executive Brief",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"## Headline",
        headline,
        "",
        "## Market Summary",
        summary_text,
        "",
        "## Core Metrics",
        f"- AI Infrastructure Index: {ai_index}",
        f"- GPU Price Index: {gpu_price_index}",
        f"- GPU Price Trend: {trend}",
        f"- Terminal Risk Score: {risk_score}",
        f"- Risk Level: {risk_level}",
        f"- Top Provider: {top_provider}",
        f"- Live Data Quality: {quality.get('live_data_quality_score', 'n/a')}",
        f"- GPU Scarcity Index: {scarcity.get('gpu_scarcity_index', 'n/a')}",
        f"- Frontier GPU Index: {frontier.get('frontier_gpu_index', 'n/a')}",
        "",
        "## Top Signals",
        *[f"- {item.get('severity', 'n/a').upper()}: {item.get('title', '')}" for item in top_signals],
        "",
        "## Recommended Actions",
        *[f"- {item.get('priority', 'n/a').upper()}: {item.get('title', '')}" for item in top_recommendations],
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "executive_brief",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "summary": summary_text,
        "core_metrics": {
            "ai_infrastructure_index": ai_index,
            "gpu_price_index": gpu_price_index,
            "gpu_price_trend": trend,
            "terminal_risk_score": risk_score,
            "risk_level": risk_level,
            "top_provider": top_provider,
            "live_data_quality_score": quality.get("live_data_quality_score"),
            "gpu_scarcity_index": scarcity.get("gpu_scarcity_index"),
            "frontier_gpu_index": frontier.get("frontier_gpu_index")
        },
        "top_signals": top_signals,
        "recommended_actions": top_recommendations,
        "markdown": "\n".join(markdown)
    }


def build_terminal_summary():
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    risk = read_latest(DATA_DIR / "terminal_risk_score.csv")
    quality = read_latest(DATA_DIR / "live_data_quality_score.csv")
    pulse = read_latest(DATA_DIR / "ai_infrastructure_pulse.csv")
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    frontier = read_latest(DATA_DIR / "frontier_gpu_index.csv")

    return {
        "product": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "status": "ok" if terminal else "degraded",
        "terminal": terminal,
        "risk": risk,
        "quality": quality,
        "pulse": pulse,
        "scarcity": scarcity,
        "frontier": frontier
    }


def build_dashboard_snapshot():
    return {
        **build_terminal_summary(),
        "signals": build_market_signals()["signals"],
        "recommendations": [],
        "executive_brief": {
            "headline": "Executive brief requires Pro access",
            "summary": "Add a Pro or Enterprise API key in the terminal to unlock recommendations and executive reporting."
        },
        "market_share": read_records(DATA_DIR / "live_provider_market_share.csv"),
        "provider_health": read_records(DATA_DIR / "provider_health.csv"),
        "provider_comparison": read_records(DATA_DIR / "provider_comparison.csv"),
        "gpu_rankings": read_records(DATA_DIR / "live_gpu_most_expensive.csv")[:10],
        "gpu_watchlist": read_records(DATA_DIR / "gpu_watchlist_intelligence.csv"),
        "alerts": read_records(DATA_DIR / "live_gpu_alerts.csv")
    }


def build_api_catalog():
    catalog = read_records(DATA_DIR / "api_catalog.csv")
    core_endpoints = [
        {
            "endpoint": "/v1/terminal-summary",
            "category": "core",
            "description": "Stable AI-RPCT terminal summary.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/dashboard-snapshot",
            "category": "core",
            "description": "Stable dashboard payload for the web terminal.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/reports/latest",
            "category": "reports",
            "description": "Latest generated intelligence reports.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/access-status",
            "category": "access",
            "description": "Current API key plan, allowed endpoints and recent usage status.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/plan-limits",
            "category": "access",
            "description": "Published request limits for Free, Pro and Enterprise plans.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/usage-summary",
            "category": "access",
            "description": "Usage summary for the current API key.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/commercial-snapshot",
            "category": "commercial",
            "description": "Enterprise commercial dashboard with accounts, usage, limits, MRR and upgrade signals.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/sales-pipeline",
            "category": "commercial",
            "description": "Enterprise sales pipeline generated from usage, limits and account upgrade signals.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customer-admin",
            "category": "commercial",
            "description": "Enterprise customer administration snapshot with account status, plan, usage and limits.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/account-health",
            "category": "commercial",
            "description": "Enterprise account health scoring for retention, adoption and expansion operations.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/revenue-forecast",
            "category": "commercial",
            "description": "Enterprise revenue forecast combining current MRR, pipeline lift and account health risk.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/commercial-board-report",
            "category": "reports",
            "description": "Enterprise commercial board report payload with revenue, pipeline and account health.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/commercial-board-report/html",
            "category": "reports",
            "description": "PDF-ready HTML version of the enterprise commercial board report.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/audit-log",
            "category": "commercial",
            "description": "Enterprise audit trail for customer and API-key administration actions.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers",
            "category": "commercial",
            "description": "Enterprise customer onboarding endpoint that creates an account and active V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers/revoke",
            "category": "commercial",
            "description": "Enterprise customer lifecycle endpoint that revokes a V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers/reactivate",
            "category": "commercial",
            "description": "Enterprise customer lifecycle endpoint that reactivates a revoked V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/signals",
            "category": "intelligence",
            "description": "Decision signals generated from live market, price, scarcity and provider data.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/recommendations",
            "category": "intelligence",
            "description": "Actionable AI infrastructure recommendations generated from terminal signals.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/executive-brief",
            "category": "reports",
            "description": "Executive-ready market brief generated from terminal metrics, signals and recommendations.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customer-report",
            "category": "reports",
            "description": "PDF-ready customer intelligence report payload with markdown and HTML export support.",
            "tier": "enterprise"
        }
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "core_endpoints": core_endpoints,
        "legacy_catalog": catalog
    }


def build_latest_reports():
    return {
        "daily_terminal_brief": read_latest_report("daily_terminal_brief_*.txt"),
        "weekly_infrastructure_report": read_latest_report("weekly_infrastructure_report_*.txt"),
        "market_intelligence_snapshot": read_latest_report("market_intelligence_snapshot_*.txt"),
        "executive_ai_memo": read_latest_report("executive_ai_infrastructure_memo_*.txt"),
        "investor_snapshot": read_latest_report("investor_snapshot_*.txt")
    }
