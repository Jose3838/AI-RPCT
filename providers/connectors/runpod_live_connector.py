import os
import requests
from dotenv import load_dotenv

from providers.connectors.base_connector import BaseProviderConnector


load_dotenv(".env")


class RunPodLiveConnector(BaseProviderConnector):

    provider_name = "runpod"

    def fetch(self):
        api_key = os.getenv("RUNPOD_API_KEY")

        if not api_key:
            return {
                "provider": "runpod",
                "gpu_type": "RTX 4090",
                "price_per_hour": 0.48,
                "available_capacity": 96,
                "health_score": 92,
                "region": "global",
                "source": "runpod_fallback_demo"
            }

        try:
            response = requests.get(
                "https://rest.runpod.io/v1/pods",
                headers={
                    "Authorization": f"Bearer {api_key}"
                },
                timeout=15
            )

            response.raise_for_status()
            data = response.json()

            pods = data if isinstance(data, list) else data.get("data", [])

            return {
                "provider": "runpod",
                "gpu_type": "mixed",
                "price_per_hour": 0.48,
                "available_capacity": len(pods),
                "health_score": 92,
                "region": "global",
                "source": "runpod_live_api"
            }

        except Exception as error:
            return {
                "provider": "runpod",
                "gpu_type": "RTX 4090",
                "price_per_hour": 0.48,
                "available_capacity": 96,
                "health_score": 88,
                "region": "global",
                "source": "runpod_live_error_fallback",
                "error": str(error)
            }
