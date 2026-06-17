from providers.connectors.collector import collect_provider_data


def build_provider_stability_score():

    providers = collect_provider_data()

    scores = []

    for provider in providers:

        health = provider.get(
            "health_score",
            0
        )

        capacity = provider.get(
            "available_capacity",
            0
        )

        score = round(
            (health * 0.7)
            +
            (min(capacity, 100) * 0.3),
            2
        )

        scores.append({
            "provider":
                provider["provider"],
            "stability_score":
                score
        })

    scores = sorted(
        scores,
        key=lambda x:
            x["stability_score"],
        reverse=True
    )

    return {
        "status": "ok",
        "version": "v1",
        "provider_rankings": scores
    }
