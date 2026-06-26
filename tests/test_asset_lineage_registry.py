from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "asset_lineage_registry.csv"
WAREHOUSE = ROOT / "warehouse" / "metadata" / "asset_lineage_registry.csv"


def test_asset_lineage_registry_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_asset_lineage_registry.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "asset lineage records" in result.stdout
    assert DATA.exists()
    assert WAREHOUSE.exists()


def test_asset_lineage_contains_decision_flow():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    pairs = {
        (row["source_asset"], row["target_asset"])
        for row in rows
    }

    assert ("forecast_engine_v1_output", "decision_summary") in pairs
    assert ("decision_summary", "executive_morning_brief") in pairs
    assert ("decision_summary", "decision_history") in pairs
