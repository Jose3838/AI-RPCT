from __future__ import annotations

from collectors.providers.base import ProviderConnector


class TensorDockProvider(ProviderConnector):
    name = "tensordock"

    def fetch(self) -> list[dict]:
        return [
            {
                "provider": self.name,
                "gpu": "H100 SXM5",
                "price_per_hour": 2.25,
                "availability": 0,
                "source": "public_pricing_page",
            },
            {
                "provider": self.name,
                "gpu": "A100 SXM4",
                "price_per_hour": 1.80,
                "availability": 0,
                "source": "public_pricing_page",
            },
            {
                "provider": self.name,
                "gpu": "RTX 4090",
                "price_per_hour": 0.35,
                "availability": 0,
                "source": "public_pricing_page",
            },
        ]
