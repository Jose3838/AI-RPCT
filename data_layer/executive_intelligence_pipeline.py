from provider_coverage_engine_v3 import get_provider_coverage_v3
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores
from data_layer.market_strength_pipeline import build_dynamic_market_strength_index
from executive_intelligence_summary import build_executive_intelligence_summary


def build_dynamic_executive_intelligence_summary():
    coverage_data = get_provider_coverage_v3()
    provider_scores = build_dynamic_provider_activation_scores()
    market_strength_data = build_dynamic_market_strength_index()

    activation_scores = [
        item["activation_score"]
        for item in provider_scores
    ]

    summary = build_executive_intelligence_summary(
        coverage_data["coverage_percentage"],
        activation_scores,
        market_strength_data["market_strength_index"]
    )

    return {
        "status": "ok",
        "version": "v2",
        "provider_count": len(provider_scores),
        "coverage_status": coverage_data["coverage_status"],
        **summary
    }
