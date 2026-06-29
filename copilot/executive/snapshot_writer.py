from __future__ import annotations

from copilot.executive.snapshot_builder import (
    build_executive_snapshot,
)
from copilot.executive.snapshot_repository import (
    save_executive_snapshot,
)


def write_executive_snapshot() -> dict:
    snapshot = build_executive_snapshot()

    save_executive_snapshot(snapshot)

    return snapshot
