from __future__ import annotations

from copilot.intelligence.causal import get_causal_analysis
from copilot.intelligence.impact import get_impact_analysis
from copilot.intelligence.scenario import run_scenario


def simulate() -> dict:
    scenario = run_scenario(
        variable="pricing",
        change=10,
    )

    causal = get_causal_analysis()
    impact = get_impact_analysis()

    return {
        "summary": {
            "status": "simulation available",
        },
        "scenario": scenario,
        "causal": causal["summary"],
        "impact": impact["summary"],
    }
