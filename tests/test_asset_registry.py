from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "asset_registry.csv"
WAREHOUSE = ROOT / "warehouse" / "metadata" / "asset_registry.csv"


def test_asset_registry_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_asset_registry.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Wrote" in result.stdout
    assert DATA.exists()
    assert WAREHOUSE.exists()


def test_asset_registry_contains_assets():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) >= 6

    asset_names = {row["asset_name"] for row in rows}

    assert "decision_summary" in asset_names
    assert "decision_history" in asset_names
    assert "executive_morning_brief" in asset_names
