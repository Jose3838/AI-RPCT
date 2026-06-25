import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "forecast_explanations.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "forecast" / "forecast_explanations.csv"

REQUIRED_COLUMNS = {
    "explanation_id",
    "forecast_id",
    "primary_reason",
    "secondary_reason",
    "governance_note",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_explanation_builder_runs():
    subprocess.run([sys.executable, str(ROOT / "analytics" / "build_forecast_dataset.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "analytics" / "run_forecast_engine_v1.py")], cwd=ROOT, check=True)

    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_forecast_explanations.py")],
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


def test_governance_notes_block_ml_claims():
    for row in load_rows(CSV_PATH):
        assert "No ML inference" in row["governance_note"]
        assert "No accuracy claim" in row["governance_note"]
