from __future__ import annotations

from copilot.intelligence.execution import get_execution_plan
from copilot.intelligence.memory import remember
from copilot.intelligence.strategy import get_strategy


def run_runtime() -> dict:
    strategy = get_strategy()
    execution = get_execution_plan()

    runtime_state = {
        "summary": {
            "status": "runtime executed",
            "strategy": strategy["summary"]["strategy"],
            "execution_steps": execution["summary"]["step_count"],
        },
        "strategy": strategy["summary"],
        "execution": execution["summary"],
    }

    remember(runtime_state)

    return runtime_state
