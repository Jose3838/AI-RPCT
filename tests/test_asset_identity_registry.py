from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "asset_identity_registry.csv"


def test_asset_identity_registry_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_asset_identity_registry.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "asset identity records" in result.stdout
    assert DATA.exists()


def test_asset_identity_registry_contains_ids():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) >= 6

    ids = {row["asset_id"] for row in rows}

    assert "ASSET-0001" in ids
    assert "ASSET-0002" in ids
