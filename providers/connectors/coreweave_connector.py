from providers.connectors.base_connector import (
    BaseProviderConnector
)


class CoreWeaveConnector(
    BaseProviderConnector
):

    provider_name = "coreweave"

    def fetch(self):

        return {
            "provider": "coreweave",
            "gpu_type": "H100",
            "price_per_hour": 2.75,
            "available_capacity": 64,
            "health_score": 97,
            "region": "us"
        }
