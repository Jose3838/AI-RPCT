from __future__ import annotations

from collections import Counter

from copilot.io import load_csv


def get_analytics() -> dict:
    rows = load_csv("data/decision_history.csv")

    if not rows:
        return {
            "status": "no analytics available"
        }

    confidences = []
    recommendations = []
    confidence_trend = []

    for row in rows:
        try:
            confidence = float(row["confidence"])
            confidences.append(confidence)

            generated_at = (
                row.get("generated_at")
                or row.get("timestamp")
                or row.get("created_at")
            )

            confidence_trend.append(
                {
                    "generated_at": generated_at,
                    "confidence": confidence,
                }
            )

        except (KeyError, ValueError, TypeError):
            pass

        recommendation = row.get("recommendation")
        if recommendation:
            recommendations.append(recommendation)

    if not confidences:
        return {
            "status": "no confidence values available"
        }

    recommendation_counter = Counter(recommendations)

    most_common_recommendation = None
    recommendation_count = 0

    if recommendation_counter:
        most_common_recommendation, recommendation_count = (
            recommendation_counter.most_common(1)[0]
        )

    stability_score = None

    if recommendations:
        stability_score = round(
            recommendation_count / len(recommendations),
            2,
        )

    recommendation_distribution = dict(
        sorted(
            recommendation_counter.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    return {
        "decision_count": len(rows),
        "average_confidence": round(
            sum(confidences) / len(confidences),
            2,
        ),
        "max_confidence": max(confidences),
        "min_confidence": min(confidences),
        "unique_recommendations": len(recommendation_counter),
        "most_common_recommendation": most_common_recommendation,
        "latest_recommendation": recommendations[-1] if recommendations else None,
        "decision_stability_score": stability_score,
        "confidence_trend": confidence_trend,
        "recommendation_distribution": recommendation_distribution,
    }
