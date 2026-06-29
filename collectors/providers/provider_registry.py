from __future__ import annotations


PROVIDERS = [
    {
        "name": "vast",
        "module": "collectors.providers.vast",
        "live_module": "collectors.providers.vast_real",
        "requires_api_key": True,
        "api_key_env": "VAST_API_KEY",
        "priority": "high",
    },
    {
        "name": "runpod",
        "module": "collectors.providers.runpod",
        "live_module": "collectors.providers.runpod_real",
        "requires_api_key": True,
        "api_key_env": "RUNPOD_API_KEY",
        "priority": "high",
    },
    {
        "name": "coreweave",
        "module": "collectors.providers.coreweave",
        "live_module": None,
        "requires_api_key": False,
        "api_key_env": None,
        "priority": "high",
    },
    {
        "name": "lambda",
        "module": "collectors.providers.lambda",
        "live_module": "collectors.providers.lambda_labs",
        "requires_api_key": False,
        "api_key_env": None,
        "priority": "medium",
    },
    {
        "name": "nebius",
        "module": "collectors.providers.nebius",
        "live_module": None,
        "requires_api_key": False,
        "api_key_env": None,
        "priority": "medium",
    },
    {
        "name": "crusoe",
        "module": "collectors.providers.crusoe",
        "live_module": None,
        "requires_api_key": False,
        "api_key_env": None,
        "priority": "medium",
    },
    {
    "name": "tensordock",
    "module": "collectors.providers.tensordock",
    "live_module": "collectors.providers.tensordock_real",
    "requires_api_key": False,
    "api_key_env": None,
    "priority": "high",
},
]


def get_provider_names() -> list[str]:
    return [provider["name"] for provider in PROVIDERS]


def get_provider(name: str) -> dict | None:
    for provider in PROVIDERS:
        if provider["name"] == name:
            return provider
    return None


def get_high_priority_providers() -> list[dict]:
    return [
        provider
        for provider in PROVIDERS
        if provider["priority"] == "high"
    ]


def get_live_enabled_providers() -> list[dict]:
    return [
        provider
        for provider in PROVIDERS
        if provider["live_module"] is not None
    ]
