import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "intel_historical_gpu_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "intel" / "intel_historical_gpu_registry.csv"

REQUIRED_COLUMNS = {
    "gpu_id",
    "vendor",
    "family",
    "architecture",
    "product_name",
    "launch_date",
    "launch_year",
    "market_segment",
    "memory_type",
    "memory_gb",
    "compute_api",
    "status",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}


def load_rows():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_intel_historical_gpu_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_registry_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_registry_not_empty():
    assert len(load_rows()) > 0


def test_required_columns():
    rows = load_rows()
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_vendor_is_intel():
    assert {row["vendor"] for row in load_rows()} == {"Intel"}


def test_unique_gpu_ids():
    gpu_ids = [row["gpu_id"] for row in load_rows()]
    assert len(gpu_ids) == len(set(gpu_ids))


def test_launch_years_exist():
    for row in load_rows():
        assert row["launch_date"]
        assert row["launch_year"]
        assert row["launch_date"].startswith(row["launch_year"])


def test_source_fields_are_present():
    for row in load_rows():
        assert row["source_url"].startswith("https://")
        assert row["source_type"]
        assert row["source_confidence"] in {"high", "medium", "low"}


def test_no_duplicate_rows():
    rows = load_rows()
    fingerprints = [tuple(sorted(row.items())) for row in rows]
    assert len(fingerprints) == len(set(fingerprints))
