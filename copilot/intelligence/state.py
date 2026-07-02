from __future__ import annotations

from copilot.intelligence.memory import latest
from copilot.intelligence.runtime import run_runtime


_STATE = {
    "status": "initialized",
    "last_runtime": {},
}


def update_state() -> dict:
    runtime = run_runtime()

    _STATE["status"] = "updated"
    _STATE["last_runtime"] = runtime

    return get_state()


def get_state() -> dict:
    return {
        "summary": {
            "status": _STATE["status"],
        },
        "last_runtime": _STATE["last_runtime"],
        "latest_memory": latest(),
    }
