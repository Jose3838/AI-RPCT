from __future__ import annotations

from importlib import import_module


def load_provider(provider: dict):
    module_name = provider.get("live_module") or provider["module"]

    module = import_module(module_name)

    expected_class_name = "".join(
        part.capitalize()
        for part in provider["name"].split("_")
    ) + "Provider"

    if hasattr(module, expected_class_name):
        return getattr(module, expected_class_name)()

    for value in module.__dict__.values():
        if (
            isinstance(value, type)
            and value.__name__.endswith("Provider")
        ):
            return value()

    raise RuntimeError(
        f"No provider class found in module {module_name}"
    )
