import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "supply_chain_event_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "supply_chain" / "supply_chain_event_registry.csv"

REQUIRED_COLUMNS = {
    "event_id",
    "event_date",
    "event_type",
    "title",
    "affected_vendors",
    "description",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}

VALID_SOURCE_CONFIDENCE = {"high", "medium", "low"}
VALID_EVENT_TYPES = {
    "export_control",
    "export_control_reversal",
    "capacity_constraint",
    "supply_agreement",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_supply_chain_event_registry.py")],
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
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_unique_event_ids():
    rows = load_rows(CSV_PATH)
    ids = [row["event_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_event_dates_are_valid_and_ordered_ascending():
    rows = load_rows(CSV_PATH)
    dates = [datetime.strptime(row["event_date"], "%Y-%m-%d") for row in rows]
    assert dates == sorted(dates)


def test_event_types_are_governed():
    for row in load_rows(CSV_PATH):
        assert row["event_type"] in VALID_EVENT_TYPES


def test_source_confidence_is_governed():
    for row in load_rows(CSV_PATH):
        assert row["source_confidence"] in VALID_SOURCE_CONFIDENCE


def test_every_row_has_a_source_url():
    for row in load_rows(CSV_PATH):
        assert row["source_url"].startswith("https://")
