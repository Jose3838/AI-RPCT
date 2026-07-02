from __future__ import annotations

from copilot.intelligence.actions import get_actions
from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.planner import get_plan


def get_strategy() -> dict:
    decision = get_decision_score()
    actions = get_actions(decision)
    plan = get_plan()

    recommendation = decision["summary"]["recommendation"]

    if recommendation == "buy_now":
        strategy = "growth"

    elif recommendation == "monitor":
        strategy = "balanced"

    else:
        strategy = "defensive"

    return {
        "summary": {
            "status": "strategy available",
            "strategy": strategy,
            "investment_score": decision["summary"]["investment_score"],
        },
        "decision": decision["summary"],
        "actions": actions["summary"],
        "plan": plan["summary"],
    }
