import os
import requests
from datetime import datetime

class VastRealProvider:
    name = "vast_real"

    def fetch(self):
        api_key = os.getenv("VAST_API_KEY")

        if not api_key or api_key == "DEIN_KEY_HIER":
            print("VAST_API_KEY not configured with real key")
            return []

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

        endpoints = [
            ("POST", "https://console.vast.ai/api/v0/bundles/"),
            ("GET", "https://cloud.vast.ai/api/v1/bundles/")
        ]

        for method, url in endpoints:
            try:
                if method == "POST":
                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=20
                    )
                else:
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=20
                    )

                print(f"Trying {method} {url} -> {response.status_code}")

                response.raise_for_status()
                data = response.json()

                offers = data.get("offers", data if isinstance(data, list) else [])

                if isinstance(offers, dict):
                    offers = [offers]

                rows = []

                for item in offers:
                    rows.append({
                        "provider": self.name,
                        "gpu": item.get("gpu_name", item.get("gpu", "unknown")),
                        "price_per_hour": float(item.get("dph_total", item.get("price_per_hour", 0)) or 0),
                        "availability": 1,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                return rows

            except Exception as e:
                print(f"Vast endpoint failed: {url} | {e}")

        return []
