from __future__ import annotations


def get_knowledge() -> dict:
    domains = [
        "historical",
        "forecast",
        "capacity",
        "pricing",
        "market",
        "risk",
        "impact",
        "causal",
        "scenario",
        "simulation",
        "planner",
        "advisor",
        "actions",
        "strategy",
        "goal",
        "execution",
        "runtime",
        "state",
    ]

    return {
        "summary": {
            "status": "knowledge available",
            "domain_count": len(domains),
        },
        "domains": domains,
    }
