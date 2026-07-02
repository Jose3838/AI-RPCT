from __future__ import annotations

from copilot.forecast_intelligence import get_forecast_intelligence


def get_forecast_layer() -> dict:
    return get_forecast_intelligence()
