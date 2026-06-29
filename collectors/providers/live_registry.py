from __future__ import annotations

import os

from collectors.providers.provider_registry import PROVIDERS


def is_provider_configured(provider: dict) -> bool:
    if not provider["requires_api_key"]:
        return True

    api_key_env = provider["api_key_env"]

    if not api_key_env:
        return False

    return bool(os.getenv(api_key_env))


def get_configured_providers() -> list[dict]:
    return [
        provider
        for provider in PROVIDERS
        if is_provider_configured(provider)
    ]


def use_vast_real() -> bool:
    return bool(os.getenv("VAST_API_KEY"))
