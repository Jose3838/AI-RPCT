from __future__ import annotations

from copilot.io import load_csv


def get_provider_intelligence() -> dict:
    rows = load_csv("data/provider_entity_registry.csv")

    if not rows:
        return {
            "status": "no provider intelligence available"
        }

    active_providers = [
        row for row in rows
        if row.get("status") == "active"
    ]

    categories = {}

    for row in rows:
        category = row.get("provider_category", "").strip()

        if not category:
            continue

        categories[category] = categories.get(category, 0) + 1

    insight = (
        "Active providers are distributed across multiple infrastructure categories."
    )

    return {
        "summary": {
            "status": "provider intelligence available",
            "provider_count": len(rows),
            "active_provider_count": len(active_providers),
        },
        "metrics": {
            "provider_categories": categories,
        },
        "trends": {},
        "insights": [
            {
                "type": "provider",
                "severity": "info",
                "message": insight,
            }
        ],
    }
