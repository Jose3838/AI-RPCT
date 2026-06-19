from providers.connectors.collector import collect_provider_data

def live_coverage_tracker():
    data = collect_provider_data()
    providers = data.get("normalized_providers", data.get("providers", []))

    total = len(providers)

    live = len([
        p for p in providers
        if p.get("mode") == "live"
    ])

    coverage = round(
        live / total * 100,
        2
    ) if total else 0

    return {
        "coverage_percent": coverage,
        "live_providers": live,
        "total_providers": total
    }
