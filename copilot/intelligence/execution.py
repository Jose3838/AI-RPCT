from __future__ import annotations

from copilot.intelligence.goal import get_goals


def get_execution_plan() -> dict:
    goals = get_goals()

    execution_steps = []

    for index, goal in enumerate(goals["goals"], start=1):
        execution_steps.append(
            {
                "step": index,
                "goal": goal["goal"],
                "action": goal["next_action"],
                "status": "pending",
            }
        )

    return {
        "summary": {
            "status": "execution plan available",
            "step_count": len(execution_steps),
        },
        "steps": execution_steps,
    }
