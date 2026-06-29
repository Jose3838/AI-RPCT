from __future__ import annotations

from copilot.executive_intelligence import get_executive_intelligence


def get_change_intelligence() -> dict:
    executive = get_executive_intelligence()
    summary = executive["summary"]

    return {
        "summary": {
            "status": "change intelligence available",
            "baseline": "current executive intelligence snapshot",
        },
        "metrics": {
            "risk_score": summary["overall_risk_score"],
            "risk_severity": summary["overall_risk_severity"],
        },
        "changes": [],
        "insights": [
            {
                "type": "change",
                "severity": "info",
                "message": (
                    "Change intelligence initialized. Historical comparison "
                    "will be added after executive snapshots are persisted."
                ),
            }
        ],
    }
