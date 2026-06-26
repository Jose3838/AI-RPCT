from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUTS = [
    DATA / "asset_registry.csv",
    ROOT / "warehouse" / "metadata" / "asset_registry.csv",
]

FIELDS = [
    "asset_name",
    "category",
    "path",
]

ASSETS = [
    ("decision_summary", "decision", "data/decision_summary.csv"),
    ("decision_history", "decision", "data/decision_history.csv"),
    ("executive_morning_brief", "executive", "data/executive_morning_brief.csv"),
    ("forecast_engine_v1_output", "forecast", "data/forecast_engine_v1_output.csv"),
    ("feature_store", "feature_store", "data/feature_store.csv"),
    ("provider_entity_registry", "registry", "data/provider_entity_registry.csv"),
]


def main() -> None:
    rows = [
        {
            "asset_name": name,
            "category": category,
            "path": path,
        }
        for name, category, path in ASSETS
    ]

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Wrote {len(rows)} asset registry rows.")
    print(DATA / "asset_registry.csv")
    print(ROOT / "warehouse" / "metadata" / "asset_registry.csv")


if __name__ == "__main__":
    main()
