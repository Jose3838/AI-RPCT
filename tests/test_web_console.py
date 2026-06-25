from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

INDEX = ROOT / "web" / "index.html"
PAGES = ROOT / "web" / "pages"


def test_web_console_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_web_console.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert INDEX.exists()
    assert "Web console generated." in result.stdout


def test_web_console_pages_exist():
    expected = [
        "dashboard.html",
        "registry.html",
        "infrastructure.html",
        "forecast.html",
        "analytics.html",
        "governance.html",
        "api.html",
        "documentation.html",
    ]

    for page in expected:
        assert (PAGES / page).exists()


def test_web_console_index_contains_navigation():
    text = INDEX.read_text(encoding="utf-8")

    assert "AI-RPCT Web Console" in text
    assert "Registry Explorer" in text
    assert "Forecast Center" in text
    assert "API Explorer" in text
