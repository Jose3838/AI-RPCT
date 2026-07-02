from __future__ import annotations

from copilot.historical.service import (
    get_historical_intelligence,
)


def get_historical_layer() -> dict:
    """
    Unified Historical Intelligence Layer.

    Acts as the single entry point for all historical
    decision intelligence inside AI-RPCT.
    """

    return get_historical_intelligence()
