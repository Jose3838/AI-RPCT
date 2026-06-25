import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "historical_pricing_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "pricing" / "historical_pricing_registry.csv"

REQUIRED_COLUMNS = {
    "pricing_record_id",
    "relationship_id",
    "observation_date",
    "price_amount",
    "currency",
    "unit",
    "price_type",
    "verification_status",
    "source_id",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_pricing_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns_even_when_empty():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_pricing_registry_is_empty_by_design_v1():
    assert len(load_rows(CSV_PATH)) == 0
