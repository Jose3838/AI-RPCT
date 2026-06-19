import os

from providers.connectors.base_connector import (
    BaseProviderConnector
)


class NebiusConnector(
    BaseProviderConnector
):

    provider_name = "nebius"

    def fetch(self):

        api_key = os.getenv("NEBIUS_API_KEY")

        if not api_key:
            return {
                "provider": "nebius",
                "mode": "demo",
                "live_ready": False,
                "reason": "missing NEBIUS_API_KEY",
                "gpu_type": "H100",
                "price_per_hour": 2.35,
                "available_capacity": 58,
                "health_score": 91,
                "region": "eu"
            }

        return {
            "provider": "nebius",
            "mode": "live_ready",
            "live_ready": True,
            "reason": "NEBIUS_API_KEY detected",
            "gpu_type": None,
            "price_per_hour": None,
            "available_capacity": None,
            "health_score": None,
            "region": None
        }

