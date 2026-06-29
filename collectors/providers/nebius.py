from __future__ import annotations

from collectors.providers.base import ProviderConnector


class NebiusProvider(ProviderConnector):
    name = "nebius"

    def fetch(self) -> list[dict]:
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.60,
                "availability": 600,
                "source": "static_provider_adapter",
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.35,
                "availability": 900,
                "source": "static_provider_adapter",
            },
        ]


def collect():
    return {
        "provider": "nebius",
        "status": "planned",
        "live": False,
    }
