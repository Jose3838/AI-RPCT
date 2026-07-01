from __future__ import annotations

from collections import Counter

from copilot.io import load_csv


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_executive_insights() -> dict:
    decisions = load_csv("data/decision_history.csv")
    snapshots = load_csv("data/executive_snapshot_registry.csv")

    confidences = []
    recommendations = []
    risk_scores = []

    for row in decisions:
        confidence = _to_float(row.get("confidence"))

        if confidence is not None:
            confidences.append(confidence)

        recommendation = row.get("recommendation")
        if recommendation:
            recommendations.append(recommendation)

    for row in snapshots:
        risk_score = _to_float(row.get("risk_score"))

        if risk_score is not None:
            risk_scores.append(risk_score)

    average_confidence = None
    confidence_stable = False

    if confidences:
        average_confidence = round(
            sum(confidences) / len(confidences),
            2,
        )
        confidence_stable = len(set(confidences)) == 1

    recommendation_counter = Counter(recommendations)

    most_common_recommendation = None
    recommendation_stability = None

    if recommendation_counter:
        most_common_recommendation, count = recommendation_counter.most_common(1)[0]
        recommendation_stability = round(count / len(recommendations), 2)

    latest_risk_score = risk_scores[-1] if risk_scores else None
    first_risk_score = risk_scores[0] if risk_scores else None
    risk_delta = None

    if latest_risk_score is not None and first_risk_score is not None:
        risk_delta = latest_risk_score - first_risk_score

    insights = []

    if confidence_stable:
        insights.append(
            {
                "type": "confidence",
                "severity": "info",
                "message": (
                    "Decision confidence has remained stable across the available history."
                ),
            }
        )

    if recommendation_stability is not None:
        insights.append(
            {
                "type": "recommendation",
                "severity": "info",
                "message": (
                    f"The most common recommendation is '{most_common_recommendation}' "
                    f"with a stability score of {recommendation_stability}."
                ),
            }
        )

    if risk_delta is not None:
        severity = "info"

        if risk_delta > 0:
            severity = "warning"
        elif risk_delta < 0:
            severity = "positive"

        insights.append(
            {
                "type": "risk",
                "severity": severity,
                "message": (
                    f"Risk score changed by {risk_delta} points across the available snapshot history."
                ),
            }
        )

    return {
        "summary": {
            "status": "executive insights available",
            "decision_count": len(decisions),
            "snapshot_count": len(snapshots),
            "average_confidence": average_confidence,
            "latest_risk_score": latest_risk_score,
            "risk_delta": risk_delta,
            "most_common_recommendation": most_common_recommendation,
            "recommendation_stability": recommendation_stability,
        },
        "insights": insights,
    }
