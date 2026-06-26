from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision.explainer import build_explanation

OUTPUTS = [
    ROOT / "data" / "decision_explanations.csv",
    ROOT / "warehouse" / "decision" / "decision_explanations.csv",
]


def main() -> None:
    row = build_explanation()

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=row.keys(),
            )

            writer.writeheader()
            writer.writerow(row)

    print("Decision explanations generated.")
    print(ROOT / "data" / "decision_explanations.csv")


if __name__ == "__main__":
    main()
