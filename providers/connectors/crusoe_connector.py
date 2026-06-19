import os

from providers.connectors.base_connector import (
    BaseProviderConnector
)


class CrusoeConnector(
    BaseProviderConnector
):

    provider_name = "crusoe"

    def fetch(self):

        api_key = os.getenv("CRUSOE_API_KEY")

        if not api_key:
            return {
                "provider": "crusoe",
                "mode": "demo",
                "live_ready": False,
                "reason": "missing CRUSOE_API_KEY",
                "gpu_type": "H100",
                "price_per_hour": 2.15,
                "available_capacity": 41,
                "health_score": 89,
                "region": "us"
            }

        return {
            "provider": "crusoe",
            "mode": "live_ready",
            "live_ready": True,
            "reason": "CRUSOE_API_KEY detected",
            "gpu_type": None,
            "price_per_hour": None,
            "available_capacity": None,
            "health_score": None,
            "region": None
        }

