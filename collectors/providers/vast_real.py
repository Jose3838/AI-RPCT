import os
import requests
from datetime import datetime

class VastRealProvider:
    name = "vast_real"

    def fetch(self):
        api_key = os.getenv("VAST_API_KEY")

        if not api_key:
            print("VAST_API_KEY not configured")
            return []

        url = "https://console.vast.ai/api/v0/bundles/"

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            rows = []

            for item in data.get("offers", []):
                rows.append({
                    "provider": self.name,
                    "gpu": item.get("gpu_name", "unknown"),
                    "price_per_hour": float(
                        item.get("dph_total", 0)
                    ),
                    "availability": 1,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                })

            return rows

        except Exception as e:
            print(f"Vast real API failed: {e}")
            return []
