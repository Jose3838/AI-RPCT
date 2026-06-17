import os
import requests
from datetime import datetime

class VastRealProvider:
    name = "vast_real"

    def fetch(self):
        api_key = os.getenv("VAST_API_KEY")

        if not api_key or api_key == "1576c9bfb8ff3cc2fa08a61af922421ae98211c896edcce9dafe25b9f561003f":
            print("VAST_API_KEY not configured")
            return []

        url = "https://console.vast.ai/api/v0/bundles/"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "limit": 100,
            "type": "on-demand",
            "rentable": {"eq": True},
            "rented": {"eq": False}
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()
            offers = data.get("offers", [])

            if isinstance(offers, dict):
                offers = [offers]

            rows = []

            for item in offers:
                rows.append({
                    "provider": self.name,
                    "gpu": item.get("gpu_name", "unknown"),
                    "price_per_hour": float(item.get("dph_total", 0) or 0),
                    "availability": 1,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            return rows

        except Exception as e:
            print(f"Vast real API failed: {e}")
            return []
