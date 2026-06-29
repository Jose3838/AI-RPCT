from __future__ import annotations

from copilot.io import load_csv


SNAPSHOT_REGISTRY_PATH = "data/executive_snapshot_registry.csv"


def load_executive_snapshot_rows() -> list[dict[str, str]]:
    return load_csv(SNAPSHOT_REGISTRY_PATH)


def get_latest_executive_snapshot() -> dict[str, str] | None:
    rows = load_executive_snapshot_rows()

    if not rows:
        return None

    return rows[-1]
