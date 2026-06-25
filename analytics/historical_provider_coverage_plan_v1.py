from __future__ import annotations

from pathlib import Path

import pandas as pd

OUT = Path("data/historical_provider_coverage_plan_v1.csv")
REPORT = Path("reports/historical_provider_coverage_plan_v1.md")

PLAN = [
    {
        "priority": "critical",
        "provider": "AWS",
        "coverage_status": "missing",
        "target_data": "GPU pricing, availability, instance catalog",
        "forecast_impact": "very_high",
        "automation_priority": 1,
    },
    {
        "priority": "critical",
        "provider": "Azure",
        "coverage_status": "missing",
        "target_data": "GPU pricing, VM catalog",
        "forecast_impact": "very_high",
        "automation_priority": 2,
    },
    {
        "priority": "critical",
        "provider": "Google Cloud",
        "coverage_status": "missing",
        "target_data": "GPU pricing, accelerator catalog",
        "forecast_impact": "very_high",
        "automation_priority": 3,
    },
    {
        "priority": "high",
        "provider": "CoreWeave",
        "coverage_status": "partial",
        "target_data": "GPU inventory, pricing",
        "forecast_impact": "high",
        "automation_priority": 4,
    },
    {
        "priority": "high",
        "provider": "Lambda",
        "coverage_status": "partial",
        "target_data": "GPU pricing",
        "forecast_impact": "high",
        "automation_priority": 5,
    },
    {
        "priority": "high",
        "provider": "Crusoe",
        "coverage_status": "missing",
        "target_data": "GPU catalog",
        "forecast_impact": "medium",
        "automation_priority": 6,
    },
    {
        "priority": "medium",
        "provider": "Nebius",
        "coverage_status": "missing",
        "target_data": "GPU catalog",
        "forecast_impact": "medium",
        "automation_priority": 7,
    },
]


def main() -> None:
    df = pd.DataFrame(PLAN)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Historical Provider Coverage Plan v1",
                "",
                f"Providers planned: {len(df)}",
                "",
                "## Strategy",
                "",
                "1. Cover hyperscalers first.",
                "2. Expand specialized GPU clouds.",
                "3. Automate historical collection.",
                "4. Feed normalized data into the feature store.",
                "",
                "## Expected Outcome",
                "",
                "- Better forecast generalization",
                "- Stronger price forecasting",
                "- Higher customer confidence",
                "- Larger proprietary data moat",
            ]
        ),
        encoding="utf-8",
    )

    print("HISTORICAL PROVIDER COVERAGE PLAN V1")
    print("====================================")
    print(df)


if __name__ == "__main__":
    main()
