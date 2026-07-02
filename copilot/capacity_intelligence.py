from __future__ import annotations

from copilot.io import load_csv
from capacity_pressure_index import build_capacity_pressure_index

# Maps the real, currently-computed pressure_status (from
# capacity_pressure_index.py, itself derived from live provider/market/
# scarcity data) to a concrete recommended action. This is a
# current-state assessment, not a demand forecast: the underlying price/
# capacity history in this repo is too short (single-digit observations
# per series) to honestly support a "you will need N GPUs in M months"
# style prediction - see docs/INTELLIGENCE_ARCHITECTURE.md and
# project_decision_intelligence_sprint6 memory for why that distinction
# matters here.
_PRESSURE_ACTIONS = {
    "critical_pressure": "Scale up capacity immediately; current demand/scarcity signals indicate acute constraint.",
    "high_pressure": "Begin capacity expansion planning now; constraint signals are elevated.",
    "moderate_pressure": "Monitor closely; no immediate expansion required but conditions are tightening.",
    "low_pressure": "Current capacity appears sufficient; no urgent action indicated.",
}


def get_capacity_intelligence() -> dict:
    rows = load_csv("data/historical_capacity_registry.csv")

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

    pressure = build_capacity_pressure_index()
    pressure_status = pressure["pressure_status"]
    recommendation = _PRESSURE_ACTIONS[pressure_status]

    insights = [
        {
            "type": "capacity",
            "severity": (
                "critical" if pressure_status == "critical_pressure"
                else "high" if pressure_status == "high_pressure"
                else "medium" if pressure_status == "moderate_pressure"
                else "low"
            ),
            "message": (
                f"Capacity pressure index is {pressure['capacity_pressure_index']} "
                f"({pressure_status}). {recommendation}"
            ),
        }
    ]

    return {
        "summary": {
            "status": "capacity intelligence available",
            "capacity_records": len(rows),
            "capacity_pressure_index": pressure["capacity_pressure_index"],
            "pressure_status": pressure_status,
            "recommendation": recommendation,
        },
        "metrics": {
            "capacity_status": capacity_status,
            "availability_levels": availability_levels,
            "scarcity_index": pressure["scarcity_index"],
            "market_strength_index": pressure["market_strength_index"],
            "average_activation_score": pressure["average_activation_score"],
        },
        "trends": {},
        "insights": insights,
    }
