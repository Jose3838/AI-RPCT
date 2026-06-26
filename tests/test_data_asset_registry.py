from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_asset_registry():
    subprocess.run(
        [sys.executable, str(ROOT / "analytics/build_data_asset_registry.py")],
        check=True,
    )

    assert (ROOT / "data/data_asset_registry.csv").exists()
    assert (ROOT / "warehouse/metadata/data_asset_registry.csv").exists()
