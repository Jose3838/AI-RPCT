from __future__ import annotations

from copilot.risk_intelligence import get_risk_intelligence


def get_executive_recommendation() -> dict:
    risk = get_risk_intelligence()
    summary = risk["summary"]

    risk_severity = summary["risk_severity"]
    risk_score = summary["risk_score"]

    if risk_severity in {"high", "critical"}:
        priority = "high"
        action = "Review AI infrastructure risk exposure."
    elif risk_severity == "medium":
        priority = "medium"
        action = "Monitor AI infrastructure risk indicators."
    else:
        priority = "low"
        action = "Continue monitoring current infrastructure."

    return {
        "summary": {
            "status": "executive recommendation available",
            "priority": priority,
        },
        "recommendation": {
            "action": action,
            "reason": (
                f"Current executive risk severity is {risk_severity} "
                f"with a risk score of {risk_score}/100."
            ),
            "owner": "Infrastructure",
        },
    }
