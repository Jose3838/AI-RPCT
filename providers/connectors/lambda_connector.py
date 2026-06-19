import os
import requests
from intelligence.schemas.provider_offer import ProviderOffer

class LambdaConnector:
    name = "lambda"

    def fetch(self):
        api_key = os.getenv("LAMBDA_API_KEY")

        if not api_key:
            return {
                "provider": self.name,
                "live_ready": False,
                "mode": "demo",
                "offers": [],
                "error": "Missing LAMBDA_API_KEY"
            }

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            r = requests.get(
                "https://cloud.lambdalabs.com/api/v1/instance-types",
                headers=headers,
                timeout=20,
            )
            r.raise_for_status()
            payload = r.json()

            offers = []
            for item in payload.get("data", {}).values():
                instance_type = item.get("instance_type", {})
                gpu_description = instance_type.get("gpu_description")
                price = instance_type.get("price_cents_per_hour")

                regions = item.get("regions_with_capacity_available", [])
                available = bool(regions)

                offers.append(
                    ProviderOffer(
                        provider=self.name,
                        gpu_model=gpu_description or "unknown",
                        region=",".join(regions) if regions else None,
                        price_usd_per_gpu_hour=(price / 100) if price else None,
                        available=available,
                        source="lambda_cloud_api",
                        mode="live",
                        raw=item,
                        observed_at=ProviderOffer.now_iso(),
                    ).to_dict()
                )

            return {
                "provider": self.name,
                "live_ready": True,
                "mode": "live",
                "offers": offers,
                "error": None,
            }

        except Exception as e:
            return {
                "provider": self.name,
                "live_ready": True,
                "mode": "error",
                "offers": [],
                "error": str(e),
            }
