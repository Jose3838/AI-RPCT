from __future__ import annotations

from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "lineage_id",
    "builder",
    "output_dataset",
    "input_datasets",
]

ROWS = [
    {
        "lineage_id": "lineage000001",
        "builder": "build_feature_store.py",
        "output_dataset": "feature_store.csv",
        "input_datasets": (
            "provider_entity_registry.csv;"
            "provider_relationship_registry.csv;"
            "historical_capacity_registry.csv;"
            "unified_accelerator_registry.csv"
        ),
    },
    {
        "lineage_id": "lineage000002",
        "builder": "build_forecast_dataset.py",
        "output_dataset": "forecast_dataset.csv",
        "input_datasets": "feature_store.csv",
    },
    {
        "lineage_id": "lineage000003",
        "builder": "run_forecast_engine_v1.py",
        "output_dataset": "forecast_engine_v1_output.csv",
        "input_datasets": "forecast_dataset.csv",
    },
    {
        "lineage_id": "lineage000004",
        "builder": "build_forecast_explanations.py",
        "output_dataset": "forecast_explanations.csv",
        "input_datasets": "forecast_engine_v1_output.csv",
    },
]


def main():
    data_path = ROOT / "data" / "data_lineage_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "metadata"
        / "data_lineage_registry.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=ROWS,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(ROWS),
        label="data lineage records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
