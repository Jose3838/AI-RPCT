from __future__ import annotations

from copilot.intelligence.memory import remember
from copilot.intelligence.pipeline import run_pipeline
from copilot.intelligence.simulation import simulate
from copilot.intelligence.scenario import run_scenario


def run_workflow() -> dict:
    pipeline = run_pipeline()

    simulation = simulate()

    scenario = run_scenario(
        variable="pricing",
        change=10,
    )

    result = {
        "summary": {
            "status": "workflow completed",
        },
        "pipeline": pipeline["summary"],
        "simulation": simulation.get("summary", {}),
        "scenario": scenario.get("summary", {}),
    }

    remember(result)

    return result
