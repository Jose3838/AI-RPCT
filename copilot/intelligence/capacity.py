from __future__ import annotations

from copilot.capacity_intelligence import get_capacity_intelligence


def get_capacity_layer() -> dict:
    return get_capacity_intelligence()
