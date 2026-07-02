from __future__ import annotations

from copilot.intelligence.controller import get_controller


def get_director() -> dict:
    controller = get_controller()

    return {
        "summary": {
            "status": "director active",
            "version": "1.0",
        },
        "controller": controller,
    }
