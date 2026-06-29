from __future__ import annotations

from copilot.executive.snapshot_writer import (
    write_executive_snapshot,
)


def run_executive_snapshot() -> dict:
    snapshot = write_executive_snapshot()

    return {
        "status": "executive snapshot completed",
        "snapshot": snapshot,
    }
