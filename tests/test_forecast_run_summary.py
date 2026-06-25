import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "forecast_run_summary.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "forecast" / "forecast_run_summary.csv"

REQUIRED_COLUMNS = {
    "summary_id",
    "run_timestamp_utc",
    "forecast_output_rows",
    "governance_status",
    "ml_training_allowed",
    "production_promotion_allowed",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_forecast_run_summary_builder_runs():
    subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_forecast_dataset.py")],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "run_forecast_engine_v1.py")],
        cwd=ROOT,
        check=True,
    )

    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_forecast_run_summary.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_governance_blocks_ml_and_promotion():
    rows = load_rows(CSV_PATH)
    assert rows[0]["ml_training_allowed"] == "false"
    assert rows[0]["production_promotion_allowed"] == "false"
