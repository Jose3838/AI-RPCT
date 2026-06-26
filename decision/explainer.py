from __future__ import annotations

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def build_explanation() -> dict[str, str]:
    explanation = {
        "decision_id": "decision-001",
        "recommendation": "Reserve Capacity",
        "confidence": "0.82",
        "reason_1": "Forecast confidence is high.",
        "reason_2": "Historical decisions support the recommendation.",
        "reason_3": "Capacity risk remains elevated.",
        "reason_4": "Market trend remains positive.",
    }

    return explanation
