from __future__ import annotations


def get_status() -> dict:
    return {
        "platform_status": "healthy",
        "pipeline": "ok",
        "decision_engine": "ok",
        "forecast": "ok",
        "tests": 294,
    }
