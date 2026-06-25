import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "nvidia_historical_gpu_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "nvidia" / "nvidia_historical_gpu_registry.csv"

REQUIRED_COLUMNS = {
    "entity_id",
    "vendor",
    "product_name",
    "architecture",
    "launch_year",
    "compute_api",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "analytics" / "build_nvidia_historical_gpu_registry.py"),
        ],
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


def test_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_vendor():
    vendors = {r["vendor"] for r in load_rows(CSV_PATH)}
    assert vendors == {"NVIDIA"}


def test_unique_entity_ids():
    ids = [r["entity_id"] for r in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_compute_api():
    apis = {r["compute_api"] for r in load_rows(CSV_PATH)}
    assert apis == {"CUDA"}


def test_status():
    allowed = {"historical", "current", "deprecated"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed
