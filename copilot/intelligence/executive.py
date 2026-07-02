from __future__ import annotations

from copilot.intelligence.director import get_director


def get_executive() -> dict:
    director = get_director()

    return {
        "summary": {
            "status": "executive active",
            "version": "1.0",
        },
        "director": director,
    }
