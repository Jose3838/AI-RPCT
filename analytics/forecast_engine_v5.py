from __future__ import annotations

from pathlib import Path

import pandas as pd

V4 = Path("data/forecast_engine_v4.csv")
BASELINE = Path("data/learning_baseline_model_v1.csv")
OUT = Path("data/forecast_engine_v5.csv")
REPORT = Path("reports/forecast_engine_v5.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    v4 = read_csv(V4)
    baseline = read_csv(BASELINE)

    if v4.empty:
        raise SystemExit("forecast_engine_v4.csv missing or empty")
    if baseline.empty:
        raise SystemExit("learning_baseline_model_v1.csv missing or empty")

    merged = v4.merge(
        baseline[
            [
                "provider",
                "gpu",
                "baseline_prediction",
                "baseline_confidence",
                "support_rows",
                "training_rows",
            ]
        ],
        on=["provider", "gpu"],
        how="left",
    )

    merged["baseline_confidence"] = pd.to_numeric(
        merged["baseline_confidence"], errors="coerce"
    ).fillna(0)

    merged["forecast_score"] = pd.to_numeric(
        merged["forecast_score"], errors="coerce"
    ).fillna(0)

    rows = []

    for _, row in merged.iterrows():
        baseline_prediction = str(row.get("baseline_prediction", "unknown"))
        baseline_confidence = float(row.get("baseline_confidence", 0))
        v4_signal = str(row.get("forecast_signal", "unknown"))
        v4_score = float(row.get("forecast_score", 0))

        if baseline_prediction != "unknown" and baseline_confidence >= 70:
            final_signal = baseline_prediction
            decision_source = "learning_baseline"
            confidence = round((baseline_confidence + v4_score) / 2, 2)
        else:
            final_signal = v4_signal
            decision_source = "forecast_engine_v4"
            confidence = v4_score

        rows.append(
            {
                "model_name": "forecast_engine_v5",
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "final_forecast_signal": final_signal,
                "decision_source": decision_source,
                "confidence": confidence,
                "v4_signal": v4_signal,
                "v4_score": v4_score,
                "baseline_prediction": baseline_prediction,
                "baseline_confidence": baseline_confidence,
                "support_rows": row.get("support_rows"),
                "training_rows": row.get("training_rows"),
            }
        )

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    learning_rows = int((out["decision_source"] == "learning_baseline").sum())

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Engine v5",
                "",
                f"Rows: {len(out)}",
                f"Learning-baseline decisions: {learning_rows}",
                "",
                "## CTO Assessment",
                "",
                "Forecast Engine v5 is the first AI-RPCT forecast layer that combines multi-factor scoring with learned baseline outcomes.",
                "It prefers the learning baseline when support and confidence are strong; otherwise it falls back to Forecast Engine v4.",
                "",
                "## Next Step",
                "",
                "Add model comparison between v4, v5, and baseline using validation outcomes.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V5")
    print("==================")
    print(f"Rows: {len(out)}")
    print(f"Learning decisions: {learning_rows}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
