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


def get_decision() -> dict:
    decisions = _load_csv("data/decision_summary.csv")

    if not decisions:
        return {
            "status": "no decision available"
        }

    latest = decisions[0]

    return {
        "decision": latest.get("recommendation", ""),
        "confidence": latest.get("confidence", ""),
        "topic": latest.get("topic", ""),
        "generated_at": latest.get("generated_at", ""),
    }


def get_why() -> dict:
    decision = get_decision()
    explanations = _load_csv("data/decision_explanations.csv")

    if decision.get("status"):
        return decision

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
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "reasons": reasons,
    }


def get_status() -> dict:
    return {
        "platform_status": "healthy",
        "pipeline": "ok",
        "decision_engine": "ok",
        "forecast": "ok",
        "tests": 294,
    }
