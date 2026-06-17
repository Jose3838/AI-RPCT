from data_layer.dynamic_snapshot_pipeline import save_dynamic_market_snapshot
from provider_expansion_tracker import save_provider_expansion
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores
from provider_activation_history import append_activation_score


def run_daily_snapshot():
    market_snapshot = save_dynamic_market_snapshot()
    provider_expansion = save_provider_expansion()
    provider_scores = build_dynamic_provider_activation_scores()

    saved_scores = []

    for item in provider_scores:
        saved_scores.append(
            append_activation_score(
                item["provider"],
                item["activation_score"]
            )
        )

    return {
        "status": "ok",
        "version": "v1",
        "market_snapshot": market_snapshot,
        "provider_expansion": provider_expansion,
        "provider_activation_scores_saved": saved_scores
    }
