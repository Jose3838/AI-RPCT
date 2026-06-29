from __future__ import annotations

from datetime import datetime, timezone

from copilot.executive.intelligence import (
    get_executive_intelligence,
)
from copilot.schemas import ExecutiveSnapshot


def build_executive_snapshot() -> ExecutiveSnapshot:
    executive = get_executive_intelligence()
    summary = executive["summary"]

    return {
        "snapshot_id": datetime.now(timezone.utc).strftime(
            "snapshot-%Y%m%d%H%M%S"
        ),
        "generated_at": summary["generated_at"],
        "risk_score": summary["overall_risk_score"],
        "risk_severity": summary["overall_risk_severity"],
        "recommendation": summary["overall_recommendation"],
        "source": "executive_snapshot_builder",
    }
