from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATORS = [
    "validate_registry.py",
    "validate_registry_schema.py",
    "validate_source_registry_links.py",
]


def run_validator(script: str) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analytics" / script),
        ],
        cwd=ROOT,
        check=True,
    )


def main():
    for validator in VALIDATORS:
        print(f"Running {validator}...")
        run_validator(validator)

    print()
    print("===================================")
    print("All registry validators passed.")
    print("===================================")


if __name__ == "__main__":
    main()
