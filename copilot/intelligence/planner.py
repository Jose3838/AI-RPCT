from __future__ import annotations

from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.cycle import run_cycle


def get_plan() -> dict:
    decision = get_decision_score()
    cycle = run_cycle()

    recommendation = decision["summary"]["recommendation"]

    if recommendation == "buy_now":
        actions = [
            "Allocate capital",
            "Monitor execution",
            "Track forecast",
        ]
        priority = "high"

    elif recommendation == "monitor":
        actions = [
            "Review market",
            "Monitor pricing",
            "Wait for confirmation",
        ]
        priority = "medium"

    else:
        actions = [
            "Delay investment",
            "Monitor risk",
            "Re-evaluate later",
        ]
        priority = "low"

    return {
        "status": "planner ready",
        "priority": priority,
        "actions": actions,
        "decision": decision,
        "cycle_status": cycle["cycle"]["status"],
    }
