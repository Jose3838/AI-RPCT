import os
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector
from intelligence.schemas.provider_offer import ProviderOffer


load_dotenv(".env")


class CrusoeConnector(BaseProviderConnector):

    provider_name = "crusoe"

    def fetch(self):
        api_key = os.getenv("CRUSOE_API_KEY")

        if not api_key:
            return {
                "provider": "crusoe",
                "live_ready": False,
                "mode": "demo",
                "offers": [
                    ProviderOffer(
                        provider="crusoe",
                        gpu_model="H100",
                        region="us",
                        price_usd_per_gpu_hour=2.15,
                        available=True,
                        source="crusoe_fallback_demo",
                        mode="demo",
                        raw={
                            "reason": "missing CRUSOE_API_KEY",
                            "available_capacity": 41,
                            "health_score": 89
                        },
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                ],
                "error": "Missing CRUSOE_API_KEY"
            }

        return {
            "provider": "crusoe",
            "live_ready": True,
            "mode": "live_ready",
            "offers": [],
            "error": "CRUSOE_API_KEY configured but live fetch not implemented"
        }
