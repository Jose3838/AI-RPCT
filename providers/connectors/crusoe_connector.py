from providers.connectors.base_connector import (
    BaseProviderConnector
)


class CrusoeConnector(
    BaseProviderConnector
):

    provider_name = "crusoe"

    def fetch(self):

        return {
            "provider": "crusoe",
            "gpu_type": "H100",
            "price_per_hour": 2.60,
            "available_capacity": 44,
            "health_score": 90,
            "region": "us"
        }
