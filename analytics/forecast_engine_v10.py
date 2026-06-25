from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURES = Path("data/feature_store_v3.csv")

OUT = Path("data/forecast_engine_v10.csv")
REPORT = Path("reports/forecast_engine_v10.md")


def classify(score: int) -> str:
    if score >= 90:
        return "very_bullish"
    if score >= 75:
        return "bullish"
    if score >= 60:
        return "neutral"
    if score >= 45:
        return "bearish"
    return "very_bearish"


def main() -> None:
    if not FEATURES.exists() or FEATURES.stat().st_size <= 1:
        raise SystemExit("feature_store_v3.csv missing or empty")

    df = pd.read_csv(FEATURES)

    base = pd.to_numeric(df.get("confidence", 0), errors="coerce").fillna(0)

    historical_family = (
        pd.to_numeric(df.get("historical_family_rows", 0), errors="coerce")
        .fillna(0)
        .clip(upper=20)
    )

    historical_activity = (
        pd.to_numeric(df.get("historical_activity_score", 0), errors="coerce")
        .fillna(0)
        .clip(upper=20)
    )

    provider_coverage = (
        pd.to_numeric(df.get("provider_count", 0), errors="coerce")
        .fillna(0)
        .clip(upper=10)
    )

    event_pressure = (
        pd.to_numeric(df.get("critical_event_count", 0), errors="coerce")
        .fillna(0)
        .clip(upper=5)
    )

    score = (
        base
        + historical_family * 1.25
        + historical_activity * 1.5
        + provider_coverage * 2
        + event_pressure * 3
    )

    result = df.copy()
    result["forecast_score"] = score.clip(0, 100).round().astype(int)
    result["forecast_signal"] = result["forecast_score"].apply(classify)
    result["forecast_engine"] = "forecast_engine_v10"
    result["forecast_method"] = "feature_store_v3_historical_timeline_enriched_scoring"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Forecast Engine v10",
            "",
            f"Rows: {len(result)}",
            f"Average score: {round(result['forecast_score'].mean(), 2)}",
            "",
            "## Inputs",
            "",
            "- Feature Store v3",
            "- Historical family coverage",
            "- Historical activity score",
            "- Provider timeline coverage",
            "- Critical event pressure",
            "",
            "## CTO Assessment",
            "",
            "Forecast Engine v10 is the first forecast engine to use Feature Store v3 historical timeline enrichment.",
            "It remains explainable and should be benchmarked against v9 before promotion.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V10")
    print("===================")
    print(result[["provider", "gpu", "forecast_score", "forecast_signal"]].head())
    print()
    print("Rows:", len(result))
    print("Average score:", round(result["forecast_score"].mean(), 2))
    print("CSV:", OUT)


if __name__ == "__main__":
    main()
