from __future__ import annotations

from datetime import datetime, timezone

from copilot.change_intelligence import get_change_intelligence
from copilot.executive_intelligence import get_executive_intelligence
from copilot.executive_recommendation import get_executive_recommendation
from copilot.executive_snapshot import get_executive_snapshots
from copilot.risk_intelligence import get_risk_intelligence


def get_executive_decision_center() -> dict:
    risk = get_risk_intelligence()
    recommendation = get_executive_recommendation()
    changes = get_change_intelligence()
    snapshots = get_executive_snapshots()
    executive = get_executive_intelligence()

    return {
        "summary": {
            "status": "executive decision center available",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "overall_risk_score": risk["summary"]["risk_score"],
            "overall_risk_severity": risk["summary"]["risk_severity"],
            "priority": recommendation["summary"]["priority"],
        },
        "risk": risk,
        "recommendation": recommendation,
        "changes": changes,
        "snapshots": snapshots,
        "executive_intelligence": executive,
    }
