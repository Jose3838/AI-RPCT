from __future__ import annotations

from collections import deque

_MEMORY = deque(maxlen=100)


def remember(entry: dict) -> None:
    _MEMORY.append(entry)


def latest() -> dict:
    if not _MEMORY:
        return {}

    return _MEMORY[-1]


def history(limit: int = 10) -> list[dict]:
    return list(_MEMORY)[-limit:]


def clear() -> None:
    _MEMORY.clear()


def get_memory_summary() -> dict:
    return {
        "summary": {
            "status": "memory available",
            "entries": len(_MEMORY),
        },
        "latest": latest(),
        "history": history(),
    }
