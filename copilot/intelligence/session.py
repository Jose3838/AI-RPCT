from __future__ import annotations

from copilot.intelligence.context import get_intelligence_context


def get_intelligence_session() -> dict:
    context = get_intelligence_context()

    return {
        "summary": {
            "status": "session active",
            "version": "1.0",
        },
        "context": context,
    }
