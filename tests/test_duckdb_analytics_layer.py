import subprocess
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "warehouse" / "analytics" / "ai_rpct.duckdb"


def test_duckdb_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_duckdb_analytics_layer.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert DB_PATH.exists()
    assert "DuckDB analytics layer generated." in result.stdout


def test_duckdb_tables_exist():
    con = duckdb.connect(str(DB_PATH))
    tables = {row[0] for row in con.execute("SHOW TABLES").fetchall()}
    con.close()

    expected = {
        "feature_store",
        "forecast_dataset",
        "forecast_engine_v1_output",
        "forecast_explanations",
        "historical_capacity_registry",
        "provider_entity_registry",
        "provider_relationship_registry",
        "unified_accelerator_registry",
    }

    assert expected.issubset(tables)


def test_feature_store_query_works():
    con = duckdb.connect(str(DB_PATH))
    count = con.execute("SELECT COUNT(*) FROM feature_store").fetchone()[0]
    con.close()

    assert count >= 0
