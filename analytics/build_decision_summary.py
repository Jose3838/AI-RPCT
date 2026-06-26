from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision.engine import build_recommendation
from decision.exporters import export_csv

def main() -> None:
    decision = build_recommendation()
    export_csv(decision)

    print("Decision summary generated.")
    print("data/decision_summary.csv")
    print("warehouse/decision/decision_summary.csv")


if __name__ == "__main__":
    main()
