from live_data_migration_plan import build_live_data_migration_plan
from connector_health_dashboard import build_connector_health_dashboard
from provider_api_key_readiness import build_provider_api_key_readiness
from live_data_readiness_score import build_live_data_readiness_score


def build_live_data_migration_dashboard():
    return {
        "status": "ok",
        "version": "v1",
        "migration_plan": build_live_data_migration_plan(),
        "connector_health": build_connector_health_dashboard(),
        "api_key_readiness": build_provider_api_key_readiness(),
        "live_data_readiness": build_live_data_readiness_score()
    }
