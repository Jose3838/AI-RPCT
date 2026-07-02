from __future__ import annotations

from copilot.intelligence.memory import get_memory_summary
from copilot.intelligence.pipeline import run_pipeline
from copilot.intelligence.simulation import simulate
from copilot.intelligence.workflow import run_workflow


def run_cycle() -> dict:
    memory = get_memory_summary()
    workflow = run_workflow()
    pipeline = run_pipeline()
    simulation = simulate()

    return {
        "cycle": {
            "status": "completed",
            "steps": [
                "memory",
                "workflow",
                "pipeline",
                "simulation",
            ],
        },
        "memory": memory,
        "workflow": workflow,
        "pipeline": pipeline,
        "simulation": simulation,
    }
