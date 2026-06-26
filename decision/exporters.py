from __future__ import annotations

import csv
from pathlib import Path

from decision.models import DecisionRecommendation

ROOT = Path(__file__).resolve().parents[1]

OUTPUTS = [
    ROOT / "data" / "decision_summary.csv",
    ROOT / "warehouse" / "decision" / "decision_summary.csv",
]


def export_csv(decision: DecisionRecommendation) -> None:
    fieldnames = [
        "decision_id",
        "topic",
        "recommendation",
        "confidence",
        "rationale",
        "generated_at",
    ]

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerow(
                {
                    "decision_id": decision.decision_id,
                    "topic": decision.topic,
                    "recommendation": decision.recommendation,
                    "confidence": decision.confidence,
                    "rationale": decision.rationale,
                    "generated_at": decision.generated_at,
                }
            )
