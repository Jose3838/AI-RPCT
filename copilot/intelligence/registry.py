from __future__ import annotations


INTELLIGENCE_MODULES = [
    {
        "name": "historical",
        "status": "active",
        "category": "data",
        "description": "Historical infrastructure and GPU registry intelligence.",
    },
    {
        "name": "forecast",
        "status": "active",
        "category": "prediction",
        "description": "Forecast and forward-looking signal intelligence.",
    },
    {
        "name": "capacity",
        "status": "active",
        "category": "supply",
        "description": "Capacity availability and infrastructure supply intelligence.",
    },
    {
        "name": "risk",
        "status": "active",
        "category": "risk",
        "description": "Risk scoring and downside monitoring intelligence.",
    },
    {
        "name": "pricing",
        "status": "active",
        "category": "market",
        "description": "Pricing signal and price history intelligence.",
    },
    {
        "name": "market",
        "status": "active",
        "category": "market",
        "description": "Market movement and competitive intelligence.",
    },
    {
        "name": "decision",
        "status": "active",
        "category": "decision",
        "description": "Decision scoring and recommendation intelligence.",
    },
    {
        "name": "actions",
        "status": "active",
        "category": "execution",
        "description": "Prioritized action generation.",
    },
    {
        "name": "advisor",
        "status": "active",
        "category": "executive",
        "description": "Executive advisory layer.",
    },
    {
        "name": "strategy",
        "status": "active",
        "category": "strategy",
        "description": "Strategy selection based on decision signals.",
    },
    {
        "name": "goal",
        "status": "active",
        "category": "planning",
        "description": "Goal generation from strategy.",
    },
    {
        "name": "execution",
        "status": "active",
        "category": "execution",
        "description": "Execution plan generation from goals.",
    },
    {
        "name": "runtime",
        "status": "active",
        "category": "runtime",
        "description": "Runtime execution state.",
    },
    {
        "name": "state",
        "status": "active",
        "category": "state",
        "description": "Current intelligence state management.",
    },
    {
        "name": "knowledge",
        "status": "active",
        "category": "knowledge",
        "description": "Knowledge map of available intelligence domains.",
    },
]


def get_intelligence_registry() -> dict:
    return {
        "summary": {
            "status": "registry available",
            "module_count": len(INTELLIGENCE_MODULES),
        },
        "modules": INTELLIGENCE_MODULES,
    }
