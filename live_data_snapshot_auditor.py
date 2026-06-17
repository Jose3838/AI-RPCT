from connector_health_dashboard import build_connector_health_dashboard
from timestamp_utils import utc_timestamp


def build_live_data_snapshot_audit():
    health = build_connector_health_dashboard()

    return {
        "status": "ok",
        "version": "v1",
        "timestamp": utc_timestamp(),
        "live_connectors": health["live_connectors"],
        "fallback_connectors": health["fallback_connectors"],
        "demo_connectors": health["demo_connectors"],
        "connectors": health["connectors"]
    }
