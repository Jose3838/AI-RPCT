from __future__ import annotations

from copilot.change_intelligence import get_change_intelligence
from copilot.executive.decision_center import (
    get_executive_decision_center,
)
from copilot.executive.insights import get_executive_insights
from copilot.executive.trend import get_executive_trend
from copilot.risk_intelligence import get_risk_intelligence
from copilot.analytics import get_analytics
from copilot.decision import get_decision
from copilot.status import get_status
from copilot.summary import get_summary


def get_executive_facade() -> dict:
    decision_center = get_executive_decision_center()
    trend = get_executive_trend()
    insights = get_executive_insights()
    changes = get_change_intelligence()
    risk = get_risk_intelligence()
    analytics = get_analytics()
    decision = get_decision()
    status = get_status()
    summary = get_summary()

    snapshots = decision_center.get("snapshots", {})
    snapshot_summary = snapshots.get("summary", {})

    return {
        "status": "executive facade available",
        "summary": decision_center.get("summary", {}),
        "metadata": decision_center.get("metadata", {}),
        "priority": decision_center.get("priority"),
        "executive_health": decision_center.get("executive_health", {}),
        "kpis": decision_center.get("kpis", {}),
        "analytics": analytics,
        "alerts": changes.get("alerts", []),
        "insights": insights,
        "changes": {
            "summary": changes.get("summary", {}),
            "metrics": changes.get("metrics", {}),
            "changes": changes.get("changes", []),
            "insights": changes.get("insights", []),
        },
        "trend": {
            "summary": trend.get("summary", {}),
            "trends": trend.get("trends", {}),
            "insights": trend.get("insights", []),
        },
        "risk": risk,
        "forecast": decision_center.get("forecast", {}),
        "recommendation": decision_center.get("recommendation", {}),
        "latest_snapshot": snapshot_summary.get("latest_snapshot"),
        "snapshot_count": snapshot_summary.get("snapshot_count", 0),
    }
