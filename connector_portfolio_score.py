from connector_health_dashboard import build_connector_health_dashboard
from live_data_quality_v2 import build_live_data_quality_v2


def build_connector_portfolio_score():
    health = build_connector_health_dashboard()
    quality = build_live_data_quality_v2()

    live = health["live_connectors"]
    total = (
        health["live_connectors"]
        + health["fallback_connectors"]
        + health["demo_connectors"]
    )

    coverage_score = round((live / total) * 100, 2) if total else 0

    return {
        "status": "ok",
        "version": "v1",
        "live_connector_coverage": coverage_score,
        "live_connectors": live,
        "total_connectors": total,
        "average_live_data_quality":
            quality["average_live_data_quality"],
        "portfolio_readiness_score":
            round(
                (coverage_score * 0.6)
                +
                (quality["average_live_data_quality"] * 0.4),
                2
            )
    }
