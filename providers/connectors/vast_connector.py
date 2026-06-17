from providers.connectors.base_connector import (
    BaseProviderConnector
)


class VastConnector(
    BaseProviderConnector
):

    provider_name = "vast"

    def fetch(self):

        return {
            "provider": "vast",
            "gpu_type": "RTX 4090",
            "price_per_hour": 0.42,
            "available_capacity": 128,
            "health_score": 95,
            "region": "global"
        }
