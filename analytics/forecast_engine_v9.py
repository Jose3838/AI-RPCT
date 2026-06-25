from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURES = Path("data/feature_store_v2.csv")

OUT = Path("data/forecast_engine_v9.csv")
REPORT = Path("reports/forecast_engine_v9.md")


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
    df = pd.read_csv(FEATURES)

    score = (
        df["confidence"].fillna(0)
        + df["historical_family_rows"].clip(upper=20) * 1.5
        + df["historical_provider_count"] * 2
        + df["historical_gpu_family_count"]
    )

    score = score.clip(0, 100).round().astype(int)

    result = df.copy()
    result["forecast_score"] = score
    result["forecast_signal"] = score.apply(classify)
    result["forecast_engine"] = "forecast_engine_v9"
    result["forecast_method"] = (
        "family_generalization_plus_historical_provider_coverage"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Engine v9",
                "",
                f"Rows: {len(result)}",
                "",
                f"Average score: {round(result['forecast_score'].mean(),2)}",
                "",
                "## Improvements",
                "",
                "- Historical provider coverage",
                "- Historical GPU family coverage",
                "- Feature Store v2 integration",
                "- Explainable scoring",
                "",
                "## CTO Assessment",
                "",
                "Forecast Engine v9 is the first engine to consume the historical provider data moat.",
                "Future ML models can learn directly from these enriched features.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V9")
    print("==================")
    print(result[[
        "provider",
        "gpu",
        "forecast_score",
        "forecast_signal"
    ]].head())

    print()
    print("Rows:", len(result))
    print("Average score:", round(result["forecast_score"].mean(),2))


if __name__ == "__main__":
    main()
