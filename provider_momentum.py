from provider_market_leadership import build_provider_market_leadership


def build_provider_momentum():
    leadership = build_provider_market_leadership()

    rankings = leadership.get(
        "provider_rankings",
        []
    )

    momentum = []

    for item in rankings:
        share = item["market_share_estimate"]

        if share >= 30:
            signal = "strong_position"
        elif share >= 15:
            signal = "competitive_position"
        elif share >= 5:
            signal = "emerging_position"
        else:
            signal = "weak_position"

        momentum.append({
            "provider": item["provider"],
            "market_share_estimate": share,
            "momentum_signal": signal
        })

    return {
        "status": "ok",
        "version": "v1",
        "momentum": momentum
    }
