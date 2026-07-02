from __future__ import annotations

from copilot.intelligence.engine import get_unified_intelligence
from copilot.intelligence.lab import get_intelligence_lab
from copilot.intelligence.memory import get_memory_summary


def get_intelligence_orchestrator() -> dict:
    unified = get_unified_intelligence()
    lab = get_intelligence_lab()
    memory = get_memory_summary()

    return {
        "summary": {
            "status": "intelligence orchestrator available",
        },
        "unified": {
            "historical": unified["historical"].get("summary", {}),
            "forecast": unified["forecast"].get("summary", {}),
            "capacity": unified["capacity"].get("summary", {}),
            "risk": unified["risk"].get("summary", {}),
            "pricing": unified["pricing"].get("summary", {}),
            "market": unified["market"].get("summary", {}),
            "impact": unified["impact"].get("summary", {}),
            "causal": unified["causal"].get("summary", {}),
            "simulation": unified["simulation"].get("summary", {}),
        },
        "lab": lab["summary"],
        "memory": memory["summary"],
    }
