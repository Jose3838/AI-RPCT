from __future__ import annotations

from copilot.decision import get_decision
from copilot.io import load_csv


def get_why() -> dict:
    decision = get_decision()
    explanations = load_csv("data/decision_explanations.csv")

    if decision.get("status"):
        return decision

    reasons = []

    if explanations:
        exp = explanations[0]

        for key in (
            "reason_1",
            "reason_2",
            "reason_3",
            "reason_4",
        ):
            value = exp.get(key)

            if value:
                reasons.append(value)

    return {
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "reasons": reasons,
    }
