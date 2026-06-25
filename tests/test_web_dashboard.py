from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DASHBOARD = ROOT / "web" / "index.html"


def test_web_dashboard_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_web_dashboard.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert DASHBOARD.exists()
    assert "Web dashboard generated." in result.stdout


def test_web_dashboard_contains_core_sections():
    text = DASHBOARD.read_text(encoding="utf-8")

    assert "AI-RPCT Web Console" in text
    assert "Platform Modules Built" in text
    assert "Registry Explorer" in text
    assert "Governance Guardrails" in text
    assert "API Endpoints" in text
