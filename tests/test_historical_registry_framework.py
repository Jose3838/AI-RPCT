import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "warehouse" / "historical" / "metadata" / "historical_registry_catalog.csv"


def test_catalog_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_registry_catalog.py")],
        cwd=ROOT / "analytics",
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote registry catalog" in result.stdout


def test_catalog_exists():
    assert CATALOG.exists()


def test_catalog_has_amd_registry():
    with CATALOG.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    dataset_ids = {row["dataset_id"] for row in rows}
    assert "amd_historical_gpu_registry" in dataset_ids


def test_catalog_governance_compliant():
    with CATALOG.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    amd = next(row for row in rows if row["dataset_id"] == "amd_historical_gpu_registry")
    assert amd["governance_status"] == "compliant"
    assert amd["verification_status"] in {"verified", "partial", "pending"}
