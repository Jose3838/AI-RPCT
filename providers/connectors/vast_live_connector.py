import os
import requests
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector
from intelligence.schemas.provider_offer import ProviderOffer

load_dotenv()


class VastLiveConnector(BaseProviderConnector):

    provider_name = "vast"

    def fetch(self):
        api_key = os.getenv("VAST_API_KEY")

        if not api_key:
            return {
                "provider": "vast",
                "live_ready": False,
                "mode": "demo",
                "offers": [
                    ProviderOffer(
                        provider="vast",
                        gpu_model="RTX 4090",
                        region="global",
                        price_usd_per_gpu_hour=0.42,
                        available=True,
                        source="vast_fallback_demo",
                        mode="demo",
                        raw={},
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                ],
                "error": "Missing VAST_API_KEY",
            }

        try:
            response = requests.get(
                "https://console.vast.ai/api/v0/bundles/",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            raw_offers = data.get("offers", [])

            offers = []
            for offer in raw_offers:
                gpu_model = (
                    offer.get("gpu_name")
                    or offer.get("gpu_name_display")
                    or offer.get("gpu_type")
                    or offer.get("machine_name")
                    or "unknown"
                )

                region = (
                    offer.get("geolocation")
                    or offer.get("country")
                    or offer.get("location")
                    or "global"
                )

                price = offer.get("dph_total")
                if price is not None:
                    price = float(price)

                offers.append(
                    ProviderOffer(
                        provider="vast",
                        gpu_model=gpu_model,
                        region=region,
                        price_usd_per_gpu_hour=price,
                        available=True,
                        source="vast_live_api",
                        mode="live",
                        raw=offer,
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                )

            return {
                "provider": "vast",
                "live_ready": True,
                "mode": "live",
                "offers": offers,
                "error": None,
            }

        except Exception as error:
            return {
                "provider": "vast",
                "live_ready": True,
                "mode": "error",
                "offers": [],
                "error": str(error),
            }
