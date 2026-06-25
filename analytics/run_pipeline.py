from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "pipeline.yaml"
ANALYTICS_DIR = ROOT / "analytics"


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


def resolve_script(step: str) -> Path:
    script = ANALYTICS_DIR / script_name(step)

    if not script.exists():
        raise FileNotFoundError(
            f"Pipeline step not found: {step} "
            f"(expected {script})"
        )

    return script


def discover_available_steps() -> set[str]:
    return {
        path.stem
        for path in ANALYTICS_DIR.glob("*.py")
        if path.name != "run_pipeline.py"
    }


def validate_manifest_steps(steps: list[str]) -> None:
    available = discover_available_steps()
    missing = [
        step
        for step in steps
        if script_name(step).removesuffix(".py") not in available
    ]

    if missing:
        raise FileNotFoundError(
            "Missing pipeline step scripts: "
            + ", ".join(missing)
        )


def run(step: str) -> None:
    script = resolve_script(step)

    print(f"\n=== {script.name} ===")
    subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        check=True,
    )


def main():
    steps = load_steps(MANIFEST)

    if not steps:
        raise RuntimeError(f"No pipeline steps found in {MANIFEST}")

    validate_manifest_steps(steps)

    for step in steps:
        run(step)

    print("\n===================================")
    print("AI-RPCT pipeline completed successfully.")
    print("===================================")


if __name__ == "__main__":
    main()
