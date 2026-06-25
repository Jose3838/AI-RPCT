import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "forecast_engine_v1_output.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "forecast" / "forecast_engine_v1_output.csv"

REQUIRED_COLUMNS = {
    "forecast_id",
    "forecast_record_id",
    "provider_id",
    "entity_id",
    "rule_based_signal",
    "forecast_class",
    "confidence_level",
    "governance_status",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_engine_runs():
    subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_forecast_dataset.py")],
        cwd=ROOT,
        check=True,
    )

    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "run_forecast_engine_v1.py")],
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


def test_governance_blocks_production_claims():
    rows = load_rows(CSV_PATH)

    for row in rows:
        assert row["governance_status"] == "non_production_no_true_labels"
        assert row["confidence_level"] == "not_applicable"


def test_forecast_classes_are_governed():
    allowed = {"monitor_only", "watch"}
    for row in load_rows(CSV_PATH):
        assert row["forecast_class"] in allowed
