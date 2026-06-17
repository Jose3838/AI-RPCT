from providers.connectors.base_connector import (
    BaseProviderConnector
)


class NebiusConnector(
    BaseProviderConnector
):

    provider_name = "nebius"

    def fetch(self):

        return {
            "provider": "nebius",
            "gpu_type": "H100",
            "price_per_hour": 2.35,
            "available_capacity": 58,
            "health_score": 91,
            "region": "eu"
        }
