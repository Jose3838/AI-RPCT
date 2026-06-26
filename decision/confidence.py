from __future__ import annotations


def calculate_confidence(evidence: list[str]) -> float:
    if not evidence:
        return 0.0

    base = 0.50
    increment = min(len(evidence) * 0.08, 0.35)

    return round(base + increment, 2)
