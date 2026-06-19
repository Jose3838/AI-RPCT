import os

from providers.connectors.base_connector import (
    BaseProviderConnector
)


class CoreWeaveConnector(
    BaseProviderConnector
):

    provider_name = "coreweave"

    def fetch(self):

        api_key = os.getenv("COREWEAVE_API_KEY")

        if not api_key:
            return {
                "provider": "coreweave",
                "mode": "demo",
                "live_ready": False,
                "reason": "missing COREWEAVE_API_KEY",
                "gpu_type": "H100",
                "price_per_hour": 2.75,
                "available_capacity": 64,
                "health_score": 97,
                "region": "us"
            }

        return {
            "provider": "coreweave",
            "mode": "live_ready",
            "live_ready": True,
            "reason": "COREWEAVE_API_KEY detected",
            "gpu_type": None,
            "price_per_hour": None,
            "available_capacity": None,
            "health_score": None,
            "region": None
        }

