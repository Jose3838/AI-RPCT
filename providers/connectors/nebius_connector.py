import os
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector
from intelligence.schemas.provider_offer import ProviderOffer


load_dotenv(".env")


class NebiusConnector(BaseProviderConnector):

    provider_name = "nebius"

    def fetch(self):
        api_key = os.getenv("NEBIUS_API_KEY")

        if not api_key:
            return {
                "provider": "nebius",
                "live_ready": False,
                "mode": "demo",
                "offers": [
                    ProviderOffer(
                        provider="nebius",
                        gpu_model="H100",
                        region="eu-north1",
                        price_usd_per_gpu_hour=2.35,
                        available=True,
                        source="nebius_fallback_demo",
                        mode="demo",
                        raw={
                            "reason": "missing NEBIUS_API_KEY",
                            "api_surface": "nebius_compute_grpc",
                            "live_fetch_status": "blocked_without_key"
                        },
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                ],
                "error": "Missing NEBIUS_API_KEY"
            }

        return {
            "provider": "nebius",
            "live_ready": True,
            "mode": "live_ready",
            "offers": [],
            "error": "NEBIUS_API_KEY configured but Nebius gRPC live fetch not implemented"
        }
