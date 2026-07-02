from __future__ import annotations

from copilot.intelligence.capacity import get_capacity_layer
from copilot.intelligence.forecast import get_forecast_layer
from copilot.intelligence.historical import get_historical_layer
from copilot.intelligence.market import get_market_layer
from copilot.intelligence.pricing import get_pricing_layer
from copilot.intelligence.risk import get_risk_layer
from copilot.intelligence.impact import get_impact_analysis


def get_unified_intelligence() -> dict:
    """
    Unified Intelligence Engine.

    Collects all intelligence domains into a single
    object for downstream Decision Intelligence.
    """

    return {
        "historical": get_historical_layer(),
        "forecast": get_forecast_layer(),
        "capacity": get_capacity_layer(),
        "risk": get_risk_layer(),
        "pricing": get_pricing_layer(),
        "market": get_market_layer(),
        "impact": get_impact_analysis(),
    }
