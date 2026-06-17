from providers.connectors.base_connector import (
    BaseProviderConnector
)


class RunPodConnector(
    BaseProviderConnector
):

    provider_name = "runpod"

    def fetch(self):

        return {
            "provider": "runpod",
            "gpu_type": "RTX 4090",
            "price_per_hour": 0.48,
            "available_capacity": 96,
            "health_score": 92,
            "region": "global"
        }
