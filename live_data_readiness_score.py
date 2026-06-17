from connector_health_dashboard import build_connector_health_dashboard


def build_live_data_readiness_score():
    health = build_connector_health_dashboard()

    total = (
        health["live_connectors"]
        +
        health["fallback_connectors"]
        +
        health["demo_connectors"]
    )

    score = round(
        (
            health["live_connectors"] / total
        ) * 100,
        2
    ) if total else 0

    return {
        "status": "ok",
        "version": "v1",
        "live_data_readiness_score": score,
        "live_connectors": health["live_connectors"],
        "fallback_connectors": health["fallback_connectors"],
        "demo_connectors": health["demo_connectors"],
        "priority": "add_real_provider_api_keys"
    }
