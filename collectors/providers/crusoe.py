from __future__ import annotations

from collectors.providers.base import ProviderConnector


class CrusoeProvider(ProviderConnector):
    name = "crusoe"

    def fetch(self) -> list[dict]:
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.70,
                "availability": 500,
                "source": "static_provider_adapter",
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.45,
                "availability": 800,
                "source": "static_provider_adapter",
            },
        ]


def collect():
    return {
        "provider": "crusoe",
        "status": "planned",
        "live": False,
    }
