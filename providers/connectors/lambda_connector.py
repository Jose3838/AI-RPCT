import os
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector
from intelligence.schemas.provider_offer import ProviderOffer


load_dotenv(".env")


class LambdaConnector(BaseProviderConnector):

    provider_name = "lambda"

    def fetch(self):
        api_key = os.getenv("LAMBDA_API_KEY")

        if not api_key:
            return {
                "provider": "lambda",
                "live_ready": False,
                "mode": "demo",
                "offers": [
                    ProviderOffer(
                        provider="lambda",
                        gpu_model="H100",
                        region="us",
                        price_usd_per_gpu_hour=2.50,
                        available=True,
                        source="lambda_fallback_demo",
                        mode="demo",
                        raw={
                            "reason": "missing LAMBDA_API_KEY",
                            "available_capacity": 40,
                            "health_score": 90
                        },
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                ],
                "error": "Missing LAMBDA_API_KEY"
            }

        return {
            "provider": "lambda",
            "live_ready": True,
            "mode": "live_ready",
            "offers": [],
            "error": "LAMBDA_API_KEY configured but live fetch not implemented"
        }
