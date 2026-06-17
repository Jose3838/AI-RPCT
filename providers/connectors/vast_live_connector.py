import os
import requests
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector


load_dotenv()


class VastLiveConnector(BaseProviderConnector):

    provider_name = "vast"

    def fetch(self):
        api_key = os.getenv("VAST_API_KEY")

        if not api_key:
            return {
                "provider": "vast",
                "gpu_type": "RTX 4090",
                "price_per_hour": 0.42,
                "available_capacity": 128,
                "health_score": 95,
                "region": "global",
                "source": "vast_fallback_demo"
            }

        try:
            response = requests.get(
                "https://console.vast.ai/api/v0/bundles/",
                headers={
                    "Authorization": f"Bearer {api_key}"
                },
                timeout=15
            )

            response.raise_for_status()
            data = response.json()

            offers = data.get("offers", [])

            if not offers:
                raise ValueError("No Vast offers returned")

            prices = [
                float(offer.get("dph_total", 0))
                for offer in offers
                if offer.get("dph_total") is not None
            ]

            avg_price = round(
                sum(prices) / len(prices),
                4
            ) if prices else 0

            return {
                "provider": "vast",
                "gpu_type": "mixed",
                "price_per_hour": avg_price,
                "available_capacity": len(offers),
                "health_score": 95,
                "region": "global",
                "source": "vast_live_api"
            }

        except Exception as error:
            return {
                "provider": "vast",
                "gpu_type": "RTX 4090",
                "price_per_hour": 0.42,
                "available_capacity": 128,
                "health_score": 90,
                "region": "global",
                "source": "vast_live_error_fallback",
                "error": str(error)
            }
