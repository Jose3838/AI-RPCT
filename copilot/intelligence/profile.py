from __future__ import annotations

from copilot.intelligence.session import get_intelligence_session


def get_intelligence_profile() -> dict:
    session = get_intelligence_session()

    return {
        "summary": {
            "status": "profile available",
            "version": "1.0",
        },
        "session": session,
    }
