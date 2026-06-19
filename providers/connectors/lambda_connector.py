import os

from providers.connectors.base_connector import (
    BaseProviderConnector
)


class LambdaConnector(
    BaseProviderConnector
):

    provider_name = "lambda"

    def fetch(self):

        api_key = os.getenv("LAMBDA_API_KEY")

        if not api_key:
            return {
                "provider": "lambda",
                "mode": "demo",
                "live_ready": False,
                "reason": "missing LAMBDA_API_KEY",
                "gpu_type": "H100",
                "price_per_hour": 2.49,
                "available_capacity": 72,
                "health_score": 94,
                "region": "us"
            }

        return {
            "provider": "lambda",
            "mode": "live_ready",
            "live_ready": True,
            "reason": "LAMBDA_API_KEY detected",
            "gpu_type": None,
            "price_per_hour": None,
            "available_capacity": None,
            "health_score": None,
            "region": None
        }
