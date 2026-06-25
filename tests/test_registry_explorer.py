from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "reports" / "registry_explorer.md"


def test_registry_explorer_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_registry_explorer.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert REPORT.exists()
    assert "Registry explorer generated." in result.stdout


def test_registry_explorer_contains_table():
    text = REPORT.read_text(encoding="utf-8")

    assert "# AI-RPCT Registry Explorer" in text
    assert "| Registry | Rows | Warehouse | Status |" in text
