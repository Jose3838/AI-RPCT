from __future__ import annotations

from copilot.intelligence.decision import get_decision_score


def get_actions(decision: dict | None = None) -> dict:
    if decision is None:
        decision = get_decision_score()

    recommendation = decision["summary"]["recommendation"]
    score = decision["summary"]["investment_score"]

    actions = []

    if recommendation == "buy_now":
        actions.append(
            {
                "priority": 1,
                "action": "Increase investment exposure",
                "impact": "high",
                "reason": "Investment score exceeds buy threshold.",
            }
        )
    elif recommendation == "monitor":
        actions.append(
            {
                "priority": 1,
                "action": "Monitor market conditions",
                "impact": "medium",
                "reason": "Investment score indicates monitoring.",
            }
        )
    else:
        actions.append(
            {
                "priority": 1,
                "action": "Delay investment decision",
                "impact": "high",
                "reason": "Investment score is below threshold.",
            }
        )

    actions.append(
        {
            "priority": 2,
            "action": "Review forecast assumptions",
            "impact": "medium",
            "reason": "Validate forecast before the next decision cycle.",
        }
    )

    actions.append(
        {
            "priority": 3,
            "action": "Expand historical evidence",
            "impact": "low",
            "reason": "More historical data improves confidence.",
        }
    )

    return {
        "summary": {
            "status": "actions generated",
            "action_count": len(actions),
            "investment_score": score,
        },
        "actions": actions,
    }
