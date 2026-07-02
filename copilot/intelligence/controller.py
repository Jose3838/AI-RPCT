from __future__ import annotations

from copilot.intelligence.manager import get_manager


def get_controller() -> dict:
    manager = get_manager()

    return {
        "summary": {
            "status": "controller active",
            "version": "1.0",
        },
        "manager": manager,
    }
