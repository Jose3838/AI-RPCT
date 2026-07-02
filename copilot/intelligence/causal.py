from __future__ import annotations

from copilot.intelligence.impact import get_impact_analysis


def get_causal_analysis() -> dict:
    impact = get_impact_analysis()

    causal_chains = []

    for item in impact["impacts"]:
        causal_chains.append(
            {
                "cause": item["from"],
                "effect": item["to"],
                "relationship": item["relationship"],
                "confidence": "medium",
                "explanation": (
                    f"{item['from']} can influence {item['to']} "
                    f"through a {item['relationship']} relationship."
                ),
            }
        )

    return {
        "summary": {
            "status": "causal analysis available",
            "causal_chain_count": len(causal_chains),
        },
        "causal_chains": causal_chains,
    }
