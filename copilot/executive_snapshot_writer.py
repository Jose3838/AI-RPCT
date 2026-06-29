from __future__ import annotations

from pathlib import Path

from history.history_writer import append_row

from copilot.executive_snapshot_builder import (
    build_executive_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]

FIELDS = [
    "snapshot_id",
    "generated_at",
    "risk_score",
    "risk_severity",
    "recommendation",
    "source",
]


def write_executive_snapshot() -> dict:
    snapshot = build_executive_snapshot()

    append_row(
        ROOT / "data" / "executive_snapshot_registry.csv",
        FIELDS,
        snapshot,
    )

    return snapshot
