from providers.connectors.collector import collect_provider_data


def build_connector_health_dashboard():
    providers = collect_provider_data()

    results = []

    for item in providers:
        source = item.get("source", f'{item["provider"]}_connector')

        if "live_api" in source:
            status = "live"
        elif "fallback" in source:
            status = "fallback"
        else:
            status = "demo"

        results.append({
            "provider": item["provider"],
            "source": source,
            "status": status,
            "error": item.get("error")
        })

    live_count = len([
        item for item in results
        if item["status"] == "live"
    ])

    fallback_count = len([
        item for item in results
        if item["status"] == "fallback"
    ])

    demo_count = len([
        item for item in results
        if item["status"] == "demo"
    ])

    return {
        "status": "ok",
        "version": "v1",
        "live_connectors": live_count,
        "fallback_connectors": fallback_count,
        "demo_connectors": demo_count,
        "connectors": results
    }
