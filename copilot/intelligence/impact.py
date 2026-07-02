from __future__ import annotations

from copilot.intelligence.graph import get_intelligence_graph


def get_impact_analysis() -> dict:
    graph = get_intelligence_graph()

    impacts = []

    for edge in graph["edges"]:
        impacts.append(
            {
                "from": edge["source"],
                "to": edge["target"],
                "relationship": edge["relationship"],
                "impact_strength": "medium",
            }
        )

    return {
        "summary": {
            "status": "impact analysis available",
            "impact_count": len(impacts),
        },
        "impacts": impacts,
    }
