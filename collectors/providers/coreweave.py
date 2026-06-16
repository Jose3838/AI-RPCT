from collectors.providers.base import ProviderConnector

class CoreWeaveProvider(ProviderConnector):
    name = "coreweave"

    def fetch(self):
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.75,
                "availability": 700
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.40,
                "availability": 1200
            }
        ]
