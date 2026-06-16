from collectors.providers.base import ProviderConnector

class LambdaLabsProvider(ProviderConnector):
    name = "lambda_labs"

    def fetch(self):
        return [
            {
                "provider": self.name,
                "gpu": "H100",
                "price_per_hour": 2.50,
                "availability": 800
            },
            {
                "provider": self.name,
                "gpu": "A100",
                "price_per_hour": 1.25,
                "availability": 1400
            }
        ]
