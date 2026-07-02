from __future__ import annotations

from copilot.risk_intelligence import get_risk_intelligence


def get_risk_layer() -> dict:
    return get_risk_intelligence()
