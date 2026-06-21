import os
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector
from intelligence.schemas.provider_offer import ProviderOffer


load_dotenv(".env")


class CoreWeaveConnector(BaseProviderConnector):

    provider_name = "coreweave"

    def fetch(self):
        api_key = os.getenv("COREWEAVE_API_KEY")

        if not api_key:
            return {
                "provider": "coreweave",
                "live_ready": False,
                "mode": "demo",
                "offers": [
                    ProviderOffer(
                        provider="coreweave",
                        gpu_model="H100",
                        region="us",
                        price_usd_per_gpu_hour=2.75,
                        available=True,
                        source="coreweave_fallback_demo",
                        mode="demo",
                        raw={
                            "reason": "missing COREWEAVE_API_KEY",
                            "available_capacity": 64,
                            "health_score": 97
                        },
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                ],
                "error": "Missing COREWEAVE_API_KEY"
            }

        return {
            "provider": "coreweave",
            "live_ready": True,
            "mode": "live_ready",
            "offers": [],
            "error": "COREWEAVE_API_KEY configured but live fetch not implemented"
        }
