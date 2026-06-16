import os
import requests

def fetch_runpod_real():
    api_key = os.getenv("RUNPOD_API_KEY")

    if not api_key:
        return []

    # Placeholder for real RunPod endpoint integration.
    # Next step: replace URL and parsing with official RunPod API response.
    url = "https://api.runpod.io/v2"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return []

    except Exception as e:
        print(f"RunPod real API failed: {e}")
        return []
