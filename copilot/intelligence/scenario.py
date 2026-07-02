from __future__ import annotations

from copilot.intelligence.causal import get_causal_analysis


def run_scenario(
    variable: str,
    change: float,
) -> dict:
    causal = get_causal_analysis()

    affected = []

    for chain in causal["causal_chains"]:
        if chain["cause"] == variable:
            affected.append(
                {
                    "component": chain["effect"],
                    "estimated_change": change,
                    "reason": chain["relationship"],
                }
            )

    return {
        "scenario": {
            "variable": variable,
            "change_percent": change,
        },
        "affected_components": affected,
        "summary": {
            "affected_count": len(affected),
        },
    }
