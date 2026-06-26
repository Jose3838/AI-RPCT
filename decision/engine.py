from __future__ import annotations

from datetime import UTC, datetime

from decision.models import DecisionRecommendation
from decision.evidence import collect_evidence
from decision.confidence import calculate_confidence
from decision.rules import choose_recommendation


def build_rationale(evidence: list[str], confidence: float) -> str:
    if not evidence:
        return "Insufficient evidence available for a strong recommendation."

    return (
        f"Recommendation is based on {len(evidence)} evidence sources. "
        f"Calculated confidence is {confidence}."
    )


def build_recommendation() -> DecisionRecommendation:
    evidence = collect_evidence()

    confidence = calculate_confidence(evidence)

    recommendation = choose_recommendation(
        confidence=confidence,
        evidence_count=len(evidence),
    )

    rationale = build_rationale(evidence, confidence)

    return DecisionRecommendation(
        decision_id="decision-001",
        topic="AI Infrastructure",
        recommendation=recommendation,
        confidence=confidence,
        evidence=evidence,
        risks=[],
        rationale=rationale,
        generated_at=datetime.now(UTC).isoformat(),
    )


if __name__ == "__main__":
    decision = build_recommendation()

    print(decision)
