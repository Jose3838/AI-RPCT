from __future__ import annotations

import csv
from pathlib import Path

from decision.engine import build_recommendation

ROOT = Path(__file__).resolve().parents[1]

OUTPUTS = [
    ROOT / "data" / "decision_history.csv",
    ROOT / "warehouse" / "decision" / "decision_history.csv",
]


FIELDS = [
    "generated_at",
    "decision_id",
    "topic",
    "recommendation",
    "confidence",
    "rationale",
]


def append_history() -> None:
    decision = build_recommendation()

    row = {
        "generated_at": decision.generated_at,
        "decision_id": decision.decision_id,
        "topic": decision.topic,
        "recommendation": decision.recommendation,
        "confidence": decision.confidence,
        "rationale": decision.rationale,
    }

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        exists = output.exists()

        with output.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)

            if not exists:
                writer.writeheader()

            writer.writerow(row)


if __name__ == "__main__":
    append_history()
