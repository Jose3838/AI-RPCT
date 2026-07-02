from __future__ import annotations

from copilot.intelligence.cycle import run_cycle
from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.engine import get_unified_intelligence
from copilot.intelligence.graph import get_intelligence_graph


def get_intelligence_api() -> dict:
    intelligence = get_unified_intelligence()

    return {
        "status": "ok",
        "decision": get_decision_score(),
        "graph": get_intelligence_graph(),
        "cycle": run_cycle(),
        "intelligence": intelligence,
    }
