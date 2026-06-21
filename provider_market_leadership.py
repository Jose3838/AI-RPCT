from providers.connectors.collector import collect_provider_data


def build_provider_market_leadership():

    providers = collect_provider_data()

    leadership = []

    total_capacity = sum(
        p.get("available_capacity", 0)
        for p in providers
    )

    for provider in providers:

        capacity = provider.get(
            "available_capacity",
            0
        )

        market_share = round(
            (capacity / total_capacity) * 100,
            2
        ) if total_capacity else 0

        leadership.append({
            "provider":
                provider["provider"],
            "market_share_estimate":
                market_share,
            "capacity":
                capacity
        })

    leadership = sorted(
        leadership,
        key=lambda x:
            x["market_share_estimate"],
        reverse=True
    )

    leader = (
        leadership[0]["provider"]
        if leadership else None
    )

    return {
        "status": "ok",
        "version": "v1",
        "market_leader": leader,
        "provider_rankings": leadership
    }
