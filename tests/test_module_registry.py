from pathlib import Path
import subprocess
import sys
import csv

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "module_registry.csv"
WAREHOUSE = ROOT / "warehouse" / "metadata" / "module_registry.csv"


def test_module_registry_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_module_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert DATA.exists()
    assert WAREHOUSE.exists()
    assert "module registry records" in result.stdout


def test_module_registry_contains_core_layers():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    layers = {row["layer"] for row in rows}

    assert "collection" in layers
    assert "registry" in layers
    assert "forecast" in layers
    assert "intelligence" in layers
    assert "api" in layers
    assert "web" in layers
