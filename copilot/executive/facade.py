from __future__ import annotations

from copilot.change_intelligence import get_change_intelligence
from copilot.executive.decision_center import (
    get_executive_decision_center,
)
from copilot.executive.insights import get_executive_insights
from copilot.executive.trend import get_executive_trend
from copilot.risk_intelligence import get_risk_intelligence


def get_executive_facade() -> dict:
    decision_center = get_executive_decision_center()
    trend = get_executive_trend()
    insights = get_executive_insights()
    changes = get_change_intelligence()
    risk = get_risk_intelligence()

    return {
        "status": "executive facade available",
        "decision_center": decision_center,
        "trend": trend,
        "insights": insights,
        "changes": changes,
        "risk": risk,
    }
