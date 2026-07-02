from __future__ import annotations

from copilot.intelligence.registry import get_intelligence_registry


def get_intelligence_manager() -> dict:
    registry = get_intelligence_registry()

    modules = registry["modules"]

    active_modules = [
        module
        for module in modules
        if module["status"] == "active"
    ]

    return {
        "summary": {
            "status": "manager available",
            "registered_modules": len(modules),
            "active_modules": len(active_modules),
        },
        "registry": registry,
        "active_modules": active_modules,
    }
