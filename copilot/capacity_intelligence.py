from __future__ import annotations

from copilot.io import load_csv


def get_capacity_intelligence() -> dict:
    rows = load_csv("data/historical_capacity_registry.csv")

    if not rows:
        return {
            "status": "no capacity intelligence available"
        }

    capacity_status = {}
    availability_levels = {}

    for row in rows:
        status = row.get("capacity_status", "").strip()
        level = row.get("availability_level", "").strip()

        if status:
            capacity_status[status] = capacity_status.get(status, 0) + 1

        if level:
            availability_levels[level] = (
                availability_levels.get(level, 0) + 1
            )

    return {
        "summary": {
            "status": "capacity intelligence available",
            "capacity_records": len(rows),
        },
        "metrics": {
            "capacity_status": capacity_status,
            "availability_levels": availability_levels,
        },
        "trends": {},
        "insights": [],
    }
