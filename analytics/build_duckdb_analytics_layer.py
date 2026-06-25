from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]

DB_PATH = ROOT / "warehouse" / "analytics" / "ai_rpct.duckdb"

TABLES = {
    "feature_store": ROOT / "data" / "feature_store.csv",
    "forecast_dataset": ROOT / "data" / "forecast_dataset.csv",
    "forecast_engine_v1_output": ROOT / "data" / "forecast_engine_v1_output.csv",
    "forecast_explanations": ROOT / "data" / "forecast_explanations.csv",
    "historical_capacity_registry": ROOT / "data" / "historical_capacity_registry.csv",
    "provider_entity_registry": ROOT / "data" / "provider_entity_registry.csv",
    "provider_relationship_registry": ROOT / "data" / "provider_relationship_registry.csv",
    "unified_accelerator_registry": ROOT / "data" / "unified_accelerator_registry.csv",
}


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))

    for table_name, csv_path in TABLES.items():
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.execute(
            f"""
            CREATE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}')
            """
        )

    con.close()

    print("DuckDB analytics layer generated.")
    print(DB_PATH)


if __name__ == "__main__":
    main()
