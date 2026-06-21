from providers.connectors.collector import collect_provider_data

def provider_coverage_gap():

    data = collect_provider_data()
    providers = data.get("normalized_providers", [])

    gaps = []
    live = []

    for p in providers:
        provider = p.get("provider")
        mode = p.get("mode")
        offers = len(p.get("offers", []))

        item = {
            "provider": provider,
            "mode": mode,
            "offers": offers
        }

        if mode == "live":
            live.append(item)
        else:
            gaps.append(item)

    return {
        "live": live,
        "gaps": gaps,
        "gap_count": len(gaps),
        "live_count": len(live)
    }
