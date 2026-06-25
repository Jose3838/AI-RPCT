import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "oneapi_timeline.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "oneapi" / "oneapi_timeline.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "timeline_id",
    "software_stack",
    "vendor",
    "version",
    "release_date",
    "release_year",
    "lifecycle_status",
    "source_id",
    "source_url",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_oneapi_timeline.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_oneapi_timeline_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_oneapi_timeline_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_timeline_ids():
    timeline_ids = [row["timeline_id"] for row in load_rows(CSV_PATH)]
    assert len(timeline_ids) == len(set(timeline_ids))


def test_software_stack_is_oneapi():
    assert {row["software_stack"] for row in load_rows(CSV_PATH)} == {"oneAPI"}


def test_vendor_is_intel():
    assert {row["vendor"] for row in load_rows(CSV_PATH)} == {"Intel"}


def test_release_year_matches_release_date():
    for row in load_rows(CSV_PATH):
        assert row["release_date"].startswith(row["release_year"])


def test_source_ids_exist():
    timeline_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in timeline_rows:
        assert row["source_id"] in valid_source_ids


def test_source_urls_are_https():
    for row in load_rows(CSV_PATH):
        assert row["source_url"].startswith("https://")


def test_lifecycle_status_is_governed():
    allowed = {"current", "historical", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["lifecycle_status"] in allowed
