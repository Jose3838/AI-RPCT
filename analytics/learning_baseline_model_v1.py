from __future__ import annotations

from pathlib import Path

import pandas as pd

TRAINING = Path("data/training_dataset_v1.csv")
OUT = Path("data/learning_baseline_model_v1.csv")
REPORT = Path("reports/learning_baseline_model_v1.md")


def main() -> None:
    if not TRAINING.exists() or TRAINING.stat().st_size <= 1:
        raise SystemExit("training_dataset_v1.csv missing or empty")

    df = pd.read_csv(TRAINING)

    if "future_market_regime" not in df.columns:
        raise SystemExit("future_market_regime column missing")

    rows = []

    grouped = df.groupby(["provider", "gpu"], dropna=False)

    for (provider, gpu), group in grouped:
        regimes = group["future_market_regime"].dropna().astype(str)

        if regimes.empty:
            prediction = "unknown"
            confidence = 0
            support = 0
        else:
            counts = regimes.value_counts()
            prediction = counts.index[0]
            support = int(counts.iloc[0])
            confidence = round((support / len(regimes)) * 100, 2)

        rows.append(
            {
                "model_name": "learning_baseline_model_v1",
                "provider": provider,
                "gpu": gpu,
                "baseline_prediction": prediction,
                "baseline_confidence": confidence,
                "support_rows": support,
                "training_rows": len(group),
            }
        )

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    known = int((out["baseline_prediction"] != "unknown").sum())

    REPORT.write_text(
        "\n".join(
            [
                "# Learning Baseline Model v1",
                "",
                f"Rows: {len(out)}",
                f"Known predictions: {known}",
                "",
                "## CTO Assessment",
                "",
                "This model learns the most frequent observed future market regime per provider/GPU pair.",
                "It is intentionally simple and acts as a baseline for Forecast Engine v5.",
                "",
                "## Next Step",
                "",
                "Build Forecast Engine v5 and compare it against this baseline.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("LEARNING BASELINE MODEL V1")
    print("==========================")
    print(f"Rows: {len(out)}")
    print(f"Known predictions: {known}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
