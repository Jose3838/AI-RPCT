import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_source_links():

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analytics" / "validate_source_registry_links.py")
        ],
        cwd=ROOT,
        check=True,
    )
