from __future__ import annotations

from pathlib import Path

from copilot.io import load_csv
from copilot.schemas import ExecutiveSnapshot
from history.history_writer import append_row

ROOT = Path(__file__).resolve().parents[2]

SNAPSHOT_REGISTRY_PATH = "data/executive_snapshot_registry.csv"

FIELDS = [
    "snapshot_id",
    "generated_at",
    "risk_score",
    "risk_severity",
    "recommendation",
    "source",
]


def load_executive_snapshot_rows() -> list[ExecutiveSnapshot]:
    return load_csv(SNAPSHOT_REGISTRY_PATH)


def get_latest_executive_snapshot() -> ExecutiveSnapshot | None:
    rows = load_executive_snapshot_rows()

    if not rows:
        return None

    return rows[-1]


def save_executive_snapshot(
    snapshot: ExecutiveSnapshot,
) -> None:
    append_row(
        ROOT / "data" / "executive_snapshot_registry.csv",
        FIELDS,
        snapshot,
    )
