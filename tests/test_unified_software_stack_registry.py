import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "unified_software_stack_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "unified_software_stack_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "software_id",
    "software_stack",
    "vendor",
    "version",
    "release_year",
    "lifecycle_status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_unified_software_stack_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_unified_software_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_unified_software_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_software_ids():
    software_ids = [row["software_id"] for row in load_rows(CSV_PATH)]
    assert len(software_ids) == len(set(software_ids))


def test_known_software_stacks_exist():
    stacks = {row["software_stack"] for row in load_rows(CSV_PATH)}
    expected = {"CUDA", "ROCm", "oneAPI", "SynapseAI"}
    assert expected.issubset(stacks)


def test_lifecycle_status_is_governed():
    allowed = {"current", "historical", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["lifecycle_status"] in allowed


def test_source_ids_exist():
    software_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in software_rows:
        assert row["source_id"] in valid_source_ids


def test_release_year_is_four_digits():
    for row in load_rows(CSV_PATH):
        assert len(row["release_year"]) == 4
        assert row["release_year"].isdigit()
