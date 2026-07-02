from __future__ import annotations

from copilot.intelligence.actions import get_actions
from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.planner import get_plan


def get_advisor() -> dict:
    decision = get_decision_score()

    return {
        "summary": {
            "status": "advisor available",
            "recommendation": decision["summary"]["recommendation"],
            "investment_score": decision["summary"]["investment_score"],
        },
        "decision": decision,
        "explanation": {
            "summary": {
                "status": "explanation available",
            }
        },
        "actions": get_actions(decision),
        "plan": get_plan(),
    }
