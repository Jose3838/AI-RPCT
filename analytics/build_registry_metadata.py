from __future__ import annotations

import csv
from pathlib import Path

from builders.registry_builder import write_registry

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "registry_name",
    "row_count",
    "warehouse_group",
    "status",
]

WAREHOUSE_GROUPS = {
    "feature_store": "feature_store",
    "forecast_dataset": "forecast",
    "forecast_engine_v1_output": "forecast",
    "forecast_explanations": "forecast",
    "forecast_run_summary": "forecast",
    "provider_entity_registry": "historical/providers",
    "provider_relationship_registry": "historical/providers",
    "historical_capacity_registry": "historical/capacity",
}


def row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def build_rows() -> list[dict[str, str]]:
    rows = []

    for csv_file in sorted((ROOT / "data").glob("*.csv")):
        rows.append(
            {
                "registry_name": csv_file.stem,
                "row_count": str(row_count(csv_file)),
                "warehouse_group": WAREHOUSE_GROUPS.get(
                    csv_file.stem,
                    "metadata",
                ),
                "status": "active",
            }
        )

    return rows


def main():
    write_registry(
        rows=build_rows(),
        columns=COLUMNS,
        registry_name="registry_metadata",
        warehouse_group="metadata",
        label="registry metadata records",
    )


if __name__ == "__main__":
    main()

