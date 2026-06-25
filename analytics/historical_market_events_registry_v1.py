from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/historical_market_events_registry_v1.csv")
REPORT = Path("reports/historical_market_events_registry_v1.md")

ROWS = [
    {
        "event_date": "2006-11-01",
        "event_type": "gpu_architecture_release",
        "title": "NVIDIA Tesla architecture introduced",
        "category": "gpu",
        "impact_level": "high",
        "verification_status": "verified",
        "trust_grade": "A",
    },
    {
        "event_date": "2012-03-01",
        "event_type": "gpu_architecture_release",
        "title": "NVIDIA Kepler architecture introduced",
        "category": "gpu",
        "impact_level": "high",
        "verification_status": "verified",
        "trust_grade": "A",
    },
    {
        "event_date": "2016-04-01",
        "event_type": "gpu_architecture_release",
        "title": "NVIDIA Pascal architecture introduced",
        "category": "gpu",
        "impact_level": "high",
        "verification_status": "verified",
        "trust_grade": "A",
    },
    {
        "event_date": "2020-05-01",
        "event_type": "gpu_architecture_release",
        "title": "NVIDIA Ampere architecture introduced",
        "category": "gpu",
        "impact_level": "critical",
        "verification_status": "verified",
        "trust_grade": "A",
    },
    {
        "event_date": "2022-03-01",
        "event_type": "gpu_architecture_release",
        "title": "NVIDIA Hopper architecture introduced",
        "category": "gpu",
        "impact_level": "critical",
        "verification_status": "verified",
        "trust_grade": "A",
    },
]

def main():
    df = pd.DataFrame(ROWS)
    df["registry_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Historical Market Events Registry v1",
            "",
            f"Events: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This registry contains verified historical market events.",
            "Future provider, pricing and forecasting features should reference these events through the master timeline.",
        ]),
        encoding="utf-8",
    )

    print("HISTORICAL MARKET EVENTS REGISTRY V1")
    print("====================================")
    print(df)

if __name__ == "__main__":
    main()
