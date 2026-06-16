from collectors.providers.base import ProviderConnector

class ManualProvider(ProviderConnector):
    name = "manual"

    def fetch(self):
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.15,
                "availability": 1000
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.05,
                "availability": 2500
            }
        ]
