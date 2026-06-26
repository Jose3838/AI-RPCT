from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUTS = [
    DATA / "asset_identity_registry.csv",
    ROOT / "warehouse" / "metadata" / "asset_identity_registry.csv",
]

FIELDS = [
    "asset_id",
    "asset_name",
    "category",
]

ASSETS = [
    ("ASSET-0001", "decision_summary", "decision"),
    ("ASSET-0002", "decision_history", "decision"),
    ("ASSET-0003", "executive_morning_brief", "executive"),
    ("ASSET-0004", "forecast_engine_v1_output", "forecast"),
    ("ASSET-0005", "feature_store", "feature_store"),
    ("ASSET-0006", "provider_entity_registry", "registry"),
]


def main() -> None:
    rows = [
        {
            "asset_id": asset_id,
            "asset_name": asset_name,
            "category": category,
        }
        for asset_id, asset_name, category in ASSETS
    ]

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Wrote {len(rows)} asset identity records.")
    print(DATA / "asset_identity_registry.csv")


if __name__ == "__main__":
    main()
