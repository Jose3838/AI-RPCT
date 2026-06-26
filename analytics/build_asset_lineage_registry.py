from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUTS = [
    DATA / "asset_lineage_registry.csv",
    ROOT / "warehouse" / "metadata" / "asset_lineage_registry.csv",
]

FIELDS = [
    "source_asset",
    "target_asset",
    "relationship_type",
    "layer",
]

LINEAGE = [
    ("feature_store", "forecast_dataset", "feeds", "forecast"),
    ("forecast_dataset", "forecast_engine_v1_output", "feeds", "forecast"),
    ("forecast_engine_v1_output", "forecast_explanations", "explains", "forecast"),
    ("forecast_engine_v1_output", "decision_summary", "informs", "decision"),
    ("decision_summary", "executive_morning_brief", "informs", "executive"),
    ("decision_summary", "decision_history", "archives", "history"),
    ("executive_morning_brief", "asset_registry", "documented_by", "governance"),
]


def main() -> None:
    rows = [
        {
            "source_asset": source,
            "target_asset": target,
            "relationship_type": relationship,
            "layer": layer,
        }
        for source, target, relationship, layer in LINEAGE
    ]

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Wrote {len(rows)} asset lineage records.")
    print(DATA / "asset_lineage_registry.csv")
    print(ROOT / "warehouse" / "metadata" / "asset_lineage_registry.csv")


if __name__ == "__main__":
    main()
