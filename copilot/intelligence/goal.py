from __future__ import annotations

from copilot.intelligence.strategy import get_strategy


def get_goals() -> dict:
    strategy = get_strategy()
    strategy_name = strategy["summary"]["strategy"]

    if strategy_name == "growth":
        goals = [
            {
                "goal": "Increase market exposure",
                "priority": "high",
                "status": "active",
                "next_action": "Execute high-priority investment actions.",
            }
        ]
    elif strategy_name == "balanced":
        goals = [
            {
                "goal": "Maintain optionality",
                "priority": "medium",
                "status": "active",
                "next_action": "Monitor market signals before committing.",
            }
        ]
    else:
        goals = [
            {
                "goal": "Protect capital",
                "priority": "high",
                "status": "active",
                "next_action": "Delay execution and reduce downside risk.",
            }
        ]

    return {
        "summary": {
            "status": "goals available",
            "goal_count": len(goals),
            "strategy": strategy_name,
        },
        "goals": goals,
    }
