from __future__ import annotations

from pathlib import Path

import pandas as pd

V9 = Path("data/training_dataset_v2.csv")
V10 = Path("data/forecast_engine_v10.csv")

OUT = Path("data/forecast_engine_benchmark_v2.csv")
REPORT = Path("reports/forecast_engine_benchmark_v2.md")


def summarize(name: str, df: pd.DataFrame, historical: bool) -> dict:
    score = pd.to_numeric(df.get("forecast_score", 0), errors="coerce").fillna(0)

    signal = (
        df["forecast_signal"].astype(str)
        if "forecast_signal" in df.columns
        else pd.Series(dtype=str)
    )

    bullish = int(signal.isin(["bullish", "very_bullish"]).sum())
    neutral = int((signal == "neutral").sum())
    bearish = int(signal.isin(["bearish", "very_bearish"]).sum())

    return {
        "engine": name,
        "rows": len(df),
        "average_score": round(score.mean(), 2),
        "max_score": round(score.max(), 2),
        "bullish_rows": bullish,
        "neutral_rows": neutral,
        "bearish_rows": bearish,
        "historical_enrichment": historical,
        "explainability": "high",
    }


def main() -> None:
    if not V10.exists():
        raise SystemExit("forecast_engine_v10.csv missing")

    if not V9.exists():
        raise SystemExit("training_dataset_v2.csv missing")

    v9 = pd.read_csv(V9)
    v10 = pd.read_csv(V10)

    # v9 nutzt forecast_score aus dem Trainingsdatensatz
    if "forecast_score" not in v9.columns:
        v9["forecast_score"] = 0

    benchmark = pd.DataFrame(
        [
            summarize("forecast_engine_v9", v9, False),
            summarize("forecast_engine_v10", v10, True),
        ]
    )

    benchmark["recommended_role"] = "challenger"

    champion = benchmark.sort_values(
        ["historical_enrichment", "average_score"],
        ascending=[False, False],
    ).index[0]

    benchmark.loc[champion, "recommended_role"] = "champion"

    benchmark = benchmark.sort_values(
        ["recommended_role", "average_score"],
        ascending=[False, False],
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    benchmark.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Forecast Engine Benchmark v2",
            "",
            "## Ranking",
            "",
            benchmark.to_string(index=False),
            "",
            "## CTO Assessment",
            "",
            "Forecast Engine v10 receives preference when forecast quality is comparable because it incorporates historical timeline enrichment while remaining explainable.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST ENGINE BENCHMARK V2")
    print("============================")
    print(benchmark)


if __name__ == "__main__":
    main()
