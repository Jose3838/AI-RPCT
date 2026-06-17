from provider_ranking_engine import build_provider_ranking
from infrastructure_risk_signal import build_infrastructure_risk_signal
from gpu_scarcity_index import build_gpu_scarcity_index


def build_provider_recommendations():
    ranking = build_provider_ranking()
    risk = build_infrastructure_risk_signal()
    scarcity = build_gpu_scarcity_index()

    recommendations = []

    for item in ranking["rankings"]:
        if item["rank"] == 1:
            action = "primary_provider_candidate"
        elif item["activation_score"] >= 75:
            action = "strong_secondary_provider"
        elif item["activation_score"] >= 60:
            action = "monitor_for_selective_use"
        else:
            action = "avoid_unless_pricing_improves"

        recommendations.append({
            "provider": item["provider"],
            "rank": item["rank"],
            "activation_score": item["activation_score"],
            "grade": item["grade"],
            "recommended_action": action
        })

    return {
        "status": "ok",
        "version": "v1",
        "market_risk_level": risk["risk_level"],
        "scarcity_status": scarcity["scarcity_status"],
        "recommendations": recommendations
    }
