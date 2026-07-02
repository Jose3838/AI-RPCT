from __future__ import annotations

from copilot.intelligence.engine import get_unified_intelligence
from copilot.intelligence.memory import remember


def run_pipeline() -> dict:
    intelligence = get_unified_intelligence()

    snapshot = {
        "summary": {
            "status": "pipeline snapshot available",
        },
        "unified": {
            "historical": intelligence["historical"].get("summary", {}),
            "forecast": intelligence["forecast"].get("summary", {}),
            "capacity": intelligence["capacity"].get("summary", {}),
            "risk": intelligence["risk"].get("summary", {}),
            "pricing": intelligence["pricing"].get("summary", {}),
            "market": intelligence["market"].get("summary", {}),
            "impact": intelligence["impact"].get("summary", {}),
            "causal": intelligence["causal"].get("summary", {}),
            "simulation": intelligence["simulation"].get("summary", {}),
        },
    }

    remember(snapshot)

    return {
        "summary": {
            "status": "pipeline executed",
        },
        "snapshot": snapshot,
    }
