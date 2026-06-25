from __future__ import annotations

from pathlib import Path

import pandas as pd

BENCHMARK = Path("data/forecast_engine_benchmark_v2.csv")
READINESS = Path("data/customer_forecast_readiness_v1.csv")

OUT = Path("data/production_forecast_model_v2.csv")
REPORT = Path("reports/production_forecast_selector_v2.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    benchmark = read_csv(BENCHMARK)
    readiness = read_csv(READINESS)

    if benchmark.empty:
        raise SystemExit("forecast_engine_benchmark_v2.csv missing or empty")

    champion = benchmark[benchmark["recommended_role"] == "champion"].iloc[0]
    baseline = benchmark[benchmark["engine"] == "forecast_engine_v9"].iloc[0]

    production_status = "watch"
    paid_ready = False
    preview_ready = True

    if not readiness.empty:
        preview_ready = str(readiness.iloc[0].get("customer_preview_ready", True)).lower() == "true"
        paid_ready = str(readiness.iloc[0].get("paid_production_ready", False)).lower() == "true"

    row = {
        "selected_model": champion["engine"],
        "selection_type": "historically_enriched_watch_champion",
        "baseline_reference": baseline["engine"],
        "selected_average_score": champion["average_score"],
        "baseline_average_score": baseline["average_score"],
        "historical_enrichment": champion["historical_enrichment"],
        "explainability": champion["explainability"],
        "production_status": production_status,
        "customer_preview_ready": preview_ready,
        "paid_production_ready": paid_ready,
        "selection_reason": "Selected for historical timeline enrichment while remaining explainable; v9 retained as higher-score baseline reference.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Production Forecast Selector v2",
            "",
            f"Selected model: {row['selected_model']}",
            f"Selection type: {row['selection_type']}",
            f"Baseline reference: {row['baseline_reference']}",
            f"Selected average score: {row['selected_average_score']}",
            f"Baseline average score: {row['baseline_average_score']}",
            f"Production status: {production_status}",
            "",
            "## CTO Assessment",
            "",
            "Forecast Engine v10 is selected as the historically enriched watch champion.",
            "Forecast Engine v9 remains the higher-score baseline reference.",
            "No paid production claim is allowed until true outcome labels validate predictive performance.",
            "",
        ]),
        encoding="utf-8",
    )

    print("PRODUCTION FORECAST SELECTOR V2")
    print("===============================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
