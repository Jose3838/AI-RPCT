from __future__ import annotations

from copilot.intelligence.knowledge import get_knowledge
from copilot.intelligence.manager import get_intelligence_manager
from copilot.intelligence.memory import get_memory_summary
from copilot.intelligence.state import get_state


def get_intelligence_context() -> dict:
    return {
        "summary": {
            "status": "context available",
        },
        "knowledge": get_knowledge()["summary"],
        "manager": get_intelligence_manager()["summary"],
        "memory": get_memory_summary()["summary"],
        "state": get_state()["summary"],
    }
