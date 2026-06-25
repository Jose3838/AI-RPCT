import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_registry_schema_validator_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "validate_registry_schema.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Validated" in result.stdout


def test_capacity_schema_exists():
    assert (ROOT / "schemas" / "historical_capacity_registry.schema.json").exists()
