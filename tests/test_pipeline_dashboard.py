from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "reports" / "pipeline_dashboard.md"


def test_dashboard_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_pipeline_dashboard.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert REPORT.exists()
    assert "Pipeline dashboard generated." in result.stdout


def test_dashboard_contains_sections():
    text = REPORT.read_text(encoding="utf-8")

    assert "# AI-RPCT Pipeline Dashboard" in text
    assert "## Pipeline Status" in text
    assert "## Datasets" in text
    assert "## Pipeline Version" in text
