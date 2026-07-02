from __future__ import annotations

from copilot.decision import get_decision
from copilot.intelligence.decision import get_decision_score
from copilot.io import load_csv


def _reason_from_score(label: str, score: int) -> str:
    if score >= 75:
        return f"{label} signal is strong with a score of {score}."

    if score >= 60:
        return f"{label} signal is moderate with a score of {score}."

    return f"{label} signal is weak with a score of {score}."


def get_why() -> dict:
    decision = get_decision()
    explanations = load_csv("data/decision_explanations.csv")
    decision_score = get_decision_score()

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

    score_reasons = [
        _reason_from_score(
            "Historical",
            decision_score["scores"]["historical_score"],
        ),
        _reason_from_score(
            "Risk",
            decision_score["scores"]["risk_score"],
        ),
        _reason_from_score(
            "Forecast",
            decision_score["scores"]["forecast_score"],
        ),
        _reason_from_score(
            "Pricing",
            decision_score["scores"]["pricing_score"],
        ),
        _reason_from_score(
            "Capacity",
            decision_score["scores"]["capacity_score"],
        ),
        _reason_from_score(
            "Market",
            decision_score["scores"]["market_score"],
        ),
    ]

    return {
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "reasons": reasons,
        "decision_score": decision_score["summary"],
        "score_reasons": score_reasons,
    }
