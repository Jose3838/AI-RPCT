from providers.connectors.base_connector import (
    BaseProviderConnector
)


class LambdaConnector(
    BaseProviderConnector
):

    provider_name = "lambda"

    def fetch(self):

        return {
            "provider": "lambda",
            "gpu_type": "H100",
            "price_per_hour": 2.49,
            "available_capacity": 72,
            "health_score": 94,
            "region": "us"
        }
