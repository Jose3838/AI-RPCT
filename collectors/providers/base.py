class ProviderConnector:
    name = "base"

    def fetch(self):
        raise NotImplementedError("Provider must implement fetch()")
