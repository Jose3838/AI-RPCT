from connector_coverage_score import build_connector_coverage_score
from provider_api_key_readiness import build_provider_api_key_readiness


def build_live_data_migration_plan():
    coverage = build_connector_coverage_score()
    keys = build_provider_api_key_readiness()

    return {
        "status": "ok",
        "version": "v1",
        "connector_coverage_score": coverage["connector_coverage_score"],
        "api_key_readiness_percentage": keys["api_key_readiness_percentage"],
        "next_provider_priority": "vast",
        "next_actions": [
            "Add VAST_API_KEY to .env",
            "Test Vast live connector",
            "Verify source changes from vast_fallback_demo to vast_live_api",
            "Run intelligence snapshot after live data activation"
        ]
    }
