from connector_health_dashboard import (
    build_connector_health_dashboard
)


def build_historical_live_data_coverage():

    health = build_connector_health_dashboard()

    total = (
        health["live_connectors"]
        +
        health["fallback_connectors"]
        +
        health["demo_connectors"]
    )

    live = health["live_connectors"]

    live_coverage = round(
        (live / total) * 100,
        2
    ) if total else 0

    if live_coverage >= 80:
        status = "institutional_grade"

    elif live_coverage >= 50:
        status = "growing_live_dataset"

    elif live_coverage >= 20:
        status = "early_live_dataset"

    else:
        status = "demo_dominant"

    return {
        "status": "ok",
        "version": "v1",
        "historical_live_data_coverage": live_coverage,
        "coverage_status": status,
        "live_connectors": live,
        "total_connectors": total
    }
