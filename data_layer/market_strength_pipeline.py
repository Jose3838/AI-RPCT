from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores
from market_strength_index import calculate_market_strength_index


def build_dynamic_market_strength_index():
    provider_scores = build_dynamic_provider_activation_scores()

    activation_scores = [
        item["activation_score"]
        for item in provider_scores
    ]

    market_strength = calculate_market_strength_index(
        activation_scores
    )

    return {
        "status": "ok",
        "version": "v2",
        "provider_count": len(provider_scores),
        **market_strength
    }
