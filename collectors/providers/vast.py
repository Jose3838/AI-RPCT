from collectors.providers.base import ProviderConnector

class VastProvider(ProviderConnector):
    name = "vast"

    def fetch(self):
        return [
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.05,
                "availability": 2500
            }
        ]
