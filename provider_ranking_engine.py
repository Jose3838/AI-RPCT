from data_layer.provider_scoring_pipeline import (
    build_dynamic_provider_activation_scores
)


def build_provider_ranking():
    providers = build_dynamic_provider_activation_scores()

    ranked = sorted(
        providers,
        key=lambda item: item["activation_score"],
        reverse=True
    )

    results = []

    for index, item in enumerate(ranked, start=1):
        results.append({
            "rank": index,
            "provider": item["provider"],
            "gpu_type": item["gpu_type"],
            "region": item["region"],
            "activation_score": item["activation_score"],
            "grade": item["grade"],
            "status": item["status"]
        })

    leader = results[0] if results else None

    return {
        "status": "ok",
        "version": "v1",
        "leader": leader,
        "rankings": results
    }
