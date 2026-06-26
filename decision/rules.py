from __future__ import annotations


def choose_recommendation(confidence: float, evidence_count: int) -> str:
    if confidence >= 0.75 and evidence_count >= 3:
        return "Monitor closely and prepare capacity action"

    if confidence >= 0.60:
        return "Continue monitoring with elevated attention"

    return "Insufficient evidence for action"
