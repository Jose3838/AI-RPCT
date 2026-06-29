from __future__ import annotations

from copilot.io import load_csv


def get_executive_snapshots() -> dict:
    rows = load_csv("data/executive_snapshot_registry.csv")

    if not rows:
        return {
            "status": "no executive snapshots available"
        }

    return {
        "summary": {
            "status": "executive snapshots available",
            "snapshot_count": len(rows),
            "latest_snapshot": rows[-1],
        },
        "snapshots": rows,
    }
