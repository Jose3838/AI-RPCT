from collectors.providers.base import ProviderConnector


class CoreWeaveProvider(ProviderConnector):
    name = "coreweave"

    def fetch(self):
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.95,
                "availability": 500
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.20,
                "availability": 1400
            }
        ]


def collect():
    return {
        "provider": "coreweave",
        "status": "planned",
        "live": False
    }
