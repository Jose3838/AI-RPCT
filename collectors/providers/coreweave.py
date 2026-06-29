from __future__ import annotations

from collectors.providers.base import ProviderConnector


class CoreweaveProvider(ProviderConnector):
    name = "coreweave"

    def fetch(self) -> list[dict]:
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.75,
                "availability": 700,
                "source": "static_provider_adapter",
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.40,
                "availability": 1200,
                "source": "static_provider_adapter",
            },
        ]


def collect():
    return {
        "provider": "coreweave",
        "status": "planned",
        "live": False,
    }
