from __future__ import annotations

from copilot.intelligence.causal import get_causal_analysis
from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.graph import get_intelligence_graph
from copilot.intelligence.impact import get_impact_analysis
from copilot.intelligence.scenario import run_scenario
from copilot.intelligence.simulation import simulate


def get_intelligence_lab() -> dict:
    graph = get_intelligence_graph()
    impact = get_impact_analysis()
    causal = get_causal_analysis()
    scenario = run_scenario(
        variable="pricing",
        change=10,
    )
    simulation = simulate()
    decision = get_decision_score()

    return {
        "summary": {
            "status": "intelligence lab available",
        },
        "graph": graph["summary"],
        "impact": impact["summary"],
        "causal": causal["summary"],
        "scenario": scenario["summary"],
        "simulation": simulation["summary"],
        "decision": decision["summary"],
    }
