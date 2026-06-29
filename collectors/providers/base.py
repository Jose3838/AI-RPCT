from __future__ import annotations

from abc import ABC, abstractmethod

from collectors.providers.provider_schema import ProviderSnapshot


class ProviderConnector(ABC):
    name: str = "base"

    @abstractmethod
    def fetch(self) -> list[ProviderSnapshot]:
        raise NotImplementedError

    def is_configured(self) -> bool:
        return True
