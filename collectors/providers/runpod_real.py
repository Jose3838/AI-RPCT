import os
import requests
from datetime import datetime

class RunPodRealProvider:
    name = "runpod_real"

    def fetch(self):
        api_key = os.getenv("RUNPOD_API_KEY")

        if not api_key or api_key == "DEIN_RUNPOD_KEY":
            print("RUNPOD_API_KEY not configured")
            return []

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        url = "https://api.runpod.io/graphql"

        query = """
        query {
          gpuTypes {
            id
            displayName
          }
        }
        """

        try:
            response = requests.post(
                url,
                headers=headers,
                json={"query": query},
                timeout=20
            )

            print(f"Trying RunPod {url} -> {response.status_code}")
            response.raise_for_status()

            data = response.json()
            gpu_types = data.get("data", {}).get("gpuTypes", [])

            rows = []

            for item in gpu_types:
                rows.append({
                    "provider": self.name,
                    "gpu": item.get("displayName", item.get("id", "unknown")),
                    "price_per_hour": 0,
                    "availability": 1,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            return rows

        except Exception as e:
            print(f"RunPod real API failed: {e}")
            return []
