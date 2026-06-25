import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "data_lineage_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "metadata" / "data_lineage_registry.csv"

REQUIRED_COLUMNS = {
    "lineage_id",
    "builder",
    "output_dataset",
    "input_datasets",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_data_lineage_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_lineage_ids():
    ids = [row["lineage_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_core_outputs_exist():
    outputs = {row["output_dataset"] for row in load_rows(CSV_PATH)}
    expected = {
        "feature_store.csv",
        "forecast_dataset.csv",
        "forecast_engine_v1_output.csv",
        "forecast_explanations.csv",
    }
    assert expected.issubset(outputs)
