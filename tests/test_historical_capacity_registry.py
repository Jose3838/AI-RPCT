import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "historical_capacity_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "capacity" / "historical_capacity_registry.csv"
RELATIONSHIP_REGISTRY = ROOT / "data" / "provider_relationship_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "capacity_record_id",
    "relationship_id",
    "observation_date",
    "capacity_status",
    "availability_level",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_capacity_registry.py")],
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


def test_unique_capacity_record_ids():
    ids = [row["capacity_record_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_relationship_ids_exist():
    capacity_rows = load_rows(CSV_PATH)
    relationship_rows = load_rows(RELATIONSHIP_REGISTRY)
    valid_relationship_ids = {row["relationship_id"] for row in relationship_rows}

    for row in capacity_rows:
        assert row["relationship_id"] in valid_relationship_ids


def test_source_ids_exist():
    capacity_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in capacity_rows:
        assert row["source_id"] in valid_source_ids


def test_capacity_status_is_governed():
    allowed = {"available", "limited", "unavailable"}
    for row in load_rows(CSV_PATH):
        assert row["capacity_status"] in allowed


def test_availability_level_is_governed():
    allowed = {"high", "medium", "low", "unknown"}
    for row in load_rows(CSV_PATH):
        assert row["availability_level"] in allowed


def test_observation_dates_are_iso_like():
    for row in load_rows(CSV_PATH):
        assert len(row["observation_date"]) == 10
        assert row["observation_date"][4] == "-"
        assert row["observation_date"][7] == "-"
