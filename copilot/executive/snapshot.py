from __future__ import annotations

from copilot.executive.snapshot_repository import (
    load_executive_snapshot_rows,
)


def get_executive_snapshots() -> dict:
    rows = load_executive_snapshot_rows()

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
