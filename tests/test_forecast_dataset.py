import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "forecast_dataset.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "forecast" / "forecast_dataset.csv"

REQUIRED_COLUMNS = {
    "forecast_record_id",
    "feature_id",
    "provider_id",
    "entity_id",
    "vendor",
    "architecture",
    "software_stack",
    "capacity_status",
    "availability_level",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_forecast_dataset.py")],
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


def test_unique_forecast_record_ids():
    ids = [row["forecast_record_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_capacity_status_values():
    allowed = {"available", "limited", "unavailable"}
    for row in load_rows(CSV_PATH):
        assert row["capacity_status"] in allowed


def test_availability_level_values():
    allowed = {"high", "medium", "low", "unknown"}
    for row in load_rows(CSV_PATH):
        assert row["availability_level"] in allowed
