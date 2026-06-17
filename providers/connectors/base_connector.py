class BaseProviderConnector:

    provider_name = "unknown"

    def fetch(self):
        raise NotImplementedError

    def normalize(self):
        raise NotImplementedError
