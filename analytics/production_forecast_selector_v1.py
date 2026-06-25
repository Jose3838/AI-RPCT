from __future__ import annotations

from pathlib import Path

import pandas as pd

BENCHMARK = Path("data/model_benchmark_v1.csv")
GUARD = Path("data/ml_evaluation_guard_v2.csv")

OUT = Path("data/production_forecast_model_v1.csv")
REPORT = Path("reports/production_forecast_selector_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    benchmark = read_csv(BENCHMARK)
    guard = read_csv(GUARD)

    if benchmark.empty:
        raise SystemExit("model_benchmark_v1.csv missing or empty")

    champion = benchmark[benchmark["role"] == "champion"].iloc[0]

    guard_status = "unknown"
    guard_reason = "No guard result available."

    if not guard.empty:
        guard_status = str(guard.iloc[0].get("status", "unknown"))
        guard_reason = str(guard.iloc[0].get("reason", "No reason available."))

    production_status = "watch"
    if guard_status == "production_ready":
        production_status = "production_ready"
    elif guard_status == "blocked":
        production_status = "blocked"

    row = {
        "selected_model": champion["model_name"],
        "model_type": champion["model_type"],
        "validation_accuracy": champion["validation_accuracy"],
        "test_accuracy": champion["test_accuracy"],
        "benchmark_score": champion["score"],
        "explainability": champion["explainability"],
        "guard_status": guard_status,
        "production_status": production_status,
        "selection_reason": "best benchmark score with explainability tie-breaker",
        "guard_reason": guard_reason,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Production Forecast Selector v1",
                "",
                f"Selected model: {row['selected_model']}",
                f"Production status: {row['production_status']}",
                f"Validation accuracy: {row['validation_accuracy']}%",
                f"Test accuracy: {row['test_accuracy']}%",
                f"Benchmark score: {row['benchmark_score']}",
                f"Explainability: {row['explainability']}",
                "",
                "## Selection Reason",
                "",
                row["selection_reason"],
                "",
                "## Guard Reason",
                "",
                row["guard_reason"],
                "",
                "## CTO Assessment",
                "",
                "The selected model is the current production candidate, not a fully production-ready ML claim.",
                "It may be used for internal intelligence and customer previews with clear confidence language.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("PRODUCTION FORECAST SELECTOR V1")
    print("===============================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
