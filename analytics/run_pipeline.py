from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "pipeline.yaml"


def load_steps(path: Path) -> list[str]:
    steps: list[str] = []
    in_steps = False

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped == "steps:":
            in_steps = True
            continue

        if in_steps and stripped.startswith("- "):
            steps.append(stripped[2:])

    return steps


def script_name(step: str) -> str:
    if step.endswith(".py"):
        return step

    return f"{step}.py"


def run(script: str) -> None:
    print(f"\n=== {script} ===")
    subprocess.run(
        [sys.executable, str(ROOT / "analytics" / script)],
        cwd=ROOT,
        check=True,
    )


def main():
    steps = load_steps(MANIFEST)

    if not steps:
        raise RuntimeError(f"No pipeline steps found in {MANIFEST}")

    for step in steps:
        run(script_name(step))

    print("\n===================================")
    print("AI-RPCT pipeline completed successfully.")
    print("===================================")


if __name__ == "__main__":
    main()
