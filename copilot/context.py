from __future__ import annotations

from copilot.decision import get_decision
from copilot.status import get_status


def get_context() -> dict:
    status = get_status()
    decision = get_decision()

    return {
        "platform_status": status.get("platform_status"),
        "pipeline": status.get("pipeline"),
        "decision": decision.get("decision"),
        "confidence": decision.get("confidence"),
    }
