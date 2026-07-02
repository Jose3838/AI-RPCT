from __future__ import annotations

_MEMORY: list[dict] = []


def remember(snapshot: dict) -> dict:
    _MEMORY.append(snapshot)

    return {
        "summary": {
            "status": "remembered",
            "memory_count": len(_MEMORY),
        }
    }


def latest() -> dict:
    if not _MEMORY:
        return {
            "summary": {
                "status": "memory empty",
            }
        }

    return _MEMORY[-1]


def get_memory_summary() -> dict:
    return {
        "summary": {
            "status": "memory available",
            "memory_count": len(_MEMORY),
        }
    }


def get_intelligence_memory() -> dict:
    return {
        "summary": {
            "status": "memory available",
            "version": "1.0",
            "memory_count": len(_MEMORY),
        },
        "latest": latest(),
    }
