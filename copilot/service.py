from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_csv(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path

    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_why() -> dict:
    decision = _load_csv("data/decision_summary.csv")
    explanations = _load_csv("data/decision_explanations.csv")

    if not decision:
        return {
            "status": "no decision available"
        }

    latest = decision[0]

    reasons = []

    if explanations:
        exp = explanations[0]

        for key in (
            "reason_1",
            "reason_2",
            "reason_3",
            "reason_4",
        ):
            value = exp.get(key)

            if value:
                reasons.append(value)

    return {
        "decision": latest["recommendation"],
        "confidence": latest["confidence"],
        "reasons": reasons,
    }
