from __future__ import annotations

from pathlib import Path

import pandas as pd

V8 = Path("data/forecast_engine_v8.csv")
RF = Path("data/random_forest_model_v1.csv")

OUT = Path("data/model_benchmark_v1.csv")
REPORT = Path("reports/model_benchmark_v1.md")


def summarize(path: Path, model_name: str, model_type: str, explainability: str) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    df = pd.read_csv(path)

    summary = (
        df.groupby("evaluation_split")["prediction_correct"]
        .mean()
        .mul(100)
        .round(2)
    )

    train = float(summary.get("train", 0))
    validation = float(summary.get("validation", 0))
    test = float(summary.get("test", 0))

    return {
        "model_name": model_name,
        "model_type": model_type,
        "train_accuracy": train,
        "validation_accuracy": validation,
        "test_accuracy": test,
        "score": round(validation * 0.4 + test * 0.6, 2),
        "explainability": explainability,
    }


def main() -> None:
    models = [
        summarize(
            V8,
            "forecast_engine_v8",
            "rule_based_generalization",
            "high",
        ),
        summarize(
            RF,
            "random_forest_model_v1",
            "random_forest",
            "medium",
        ),
    ]

    benchmark = pd.DataFrame(models)

    benchmark = benchmark.sort_values(
        by=["score", "validation_accuracy"],
        ascending=False,
    ).reset_index(drop=True)

    if len(benchmark) >= 2:
        first = benchmark.iloc[0]
        second = benchmark.iloc[1]

        if abs(first["score"] - second["score"]) < 0.01:
            if first["explainability"] != "high" and second["explainability"] == "high":
                benchmark = benchmark.iloc[[1, 0]].reset_index(drop=True)

    benchmark["rank"] = range(1, len(benchmark) + 1)
    benchmark["role"] = [
        "champion" if i == 0 else "challenger"
        for i in range(len(benchmark))
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    benchmark.to_csv(OUT, index=False)

    champion = benchmark.iloc[0]

    REPORT.write_text(
        "\n".join(
            [
                "# Model Benchmark v1",
                "",
                f"Champion: {champion['model_name']}",
                "",
                "## Ranking",
                "",
                benchmark.to_string(index=False),
                "",
                "## CTO Assessment",
                "",
                "Models are ranked primarily by validation/test performance.",
                "When performance is effectively tied, the more explainable model is preferred.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("MODEL BENCHMARK V1")
    print("==================")
    print(benchmark)


if __name__ == "__main__":
    main()
