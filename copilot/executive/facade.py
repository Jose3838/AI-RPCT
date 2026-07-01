from __future__ import annotations

from copilot.analytics import get_analytics
from copilot.change_intelligence import get_change_intelligence
from copilot.decision import get_decision
from copilot.executive.decision_center import (
    get_executive_decision_center,
)
from copilot.executive.facade_builder import (
    build_changes,
    build_snapshot_summary,
    build_trend,
)
from copilot.executive.insights import get_executive_insights
from copilot.executive.trend import get_executive_trend
from copilot.io import load_csv
from copilot.risk_intelligence import get_risk_intelligence
from copilot.status import get_status
from copilot.summary import get_summary
from copilot.timeline import get_decision_timeline


def _build_strategic_signals(
    risk: dict,
    forecast: dict,
    analytics: dict,
    executive_health: dict,
) -> list[dict]:
    signals = []

    risk_score = risk.get("summary", {}).get("risk_score", 0)
    forecast_watch_count = forecast.get("summary", {}).get("watch_count", 0)
    stability_score = analytics.get("decision_stability_score")
    health_score = executive_health.get("score", 0)

    if health_score >= 90:
        signals.append(
            {
                "type": "platform",
                "severity": "positive",
                "label": "Stable Platform",
                "message": (
                    "Executive health is strong and platform status is stable."
                ),
            }
        )

    if risk_score >= 80:
        signals.append(
            {
                "type": "risk",
                "severity": "info",
                "label": "Risk Under Control",
                "message": f"Executive risk score is currently {risk_score}/100.",
            }
        )

    if forecast_watch_count > 0:
        signals.append(
            {
                "type": "forecast",
                "severity": "warning",
                "label": "Capacity Watch",
                "message": (
                    f"{forecast_watch_count} forecast signal(s) require "
                    "capacity monitoring."
                ),
            }
        )

    if stability_score == 1:
        signals.append(
            {
                "type": "decision",
                "severity": "positive",
                "label": "Decision Stability",
                "message": (
                    "Executive recommendations are stable across history."
                ),
            }
        )

    if not signals:
        signals.append(
            {
                "type": "platform",
                "severity": "info",
                "label": "No Strategic Signals",
                "message": "No elevated strategic signals detected.",
            }
        )

    return signals


def get_executive_facade() -> dict:
    decision_center = get_executive_decision_center()
    trend = get_executive_trend()
    insights = get_executive_insights()
    changes = get_change_intelligence()
    risk = get_risk_intelligence()
    analytics = get_analytics()
    timeline = get_decision_timeline()
    decision = get_decision()
    status = get_status()
    summary = get_summary()

    forecast_rows = load_csv("data/forecast_engine_v1_output.csv")
    registry_rows = load_csv("data/data_asset_registry.csv")

    strategic_signals = _build_strategic_signals(
        risk=risk,
        forecast=decision_center.get("forecast", {}),
        analytics=analytics,
        executive_health=decision_center.get("executive_health", {}),
    )

    snapshots = decision_center.get("snapshots", {})
    snapshot_summary = build_snapshot_summary(
        snapshots.get("summary", {})
    )

    return {
        "status": "executive facade available",
        "summary": decision_center.get("summary", {}),
        "metadata": decision_center.get("metadata", {}),
        "priority": decision_center.get("priority"),
        "executive_health": decision_center.get("executive_health", {}),
        "kpis": decision_center.get("kpis", {}),
        "analytics": analytics,
        "decision": decision,
        "platform_status": status,
        "morning_summary": summary,
        "alerts": changes.get("alerts", []),
        "strategic_signals": strategic_signals,
        "insights": insights,
        "changes": build_changes(changes),
        "trend": build_trend(trend),
        "risk": risk,
        "forecast": decision_center.get("forecast", {}),
        "recommendation": decision_center.get("recommendation", {}),
        "timeline": timeline,
        "forecast_rows": forecast_rows,
        "registry_rows": registry_rows,
        "latest_snapshot": snapshot_summary["latest_snapshot"],
        "snapshot_count": snapshot_summary["snapshot_count"],
    }
