from __future__ import annotations

from pathlib import Path

import pandas as pd

V4 = Path("data/forecast_engine_v4.csv")
V5 = Path("data/forecast_engine_v5.csv")
BASELINE = Path("data/learning_baseline_model_v1.csv")

OUT = Path("data/model_comparison_v1.csv")
REPORT = Path("reports/model_comparison_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    v4 = read_csv(V4)
    v5 = read_csv(V5)
    baseline = read_csv(BASELINE)

    rows = []

    if not v4.empty:
        rows.append({
            "model_name": "forecast_engine_v4",
            "rows": len(v4),
            "avg_confidence": round(pd.to_numeric(v4["forecast_score"], errors="coerce").fillna(0).mean(), 2),
            "learning_enabled": False,
            "model_type": "multi_factor_rule_engine",
        })

    if not v5.empty:
        rows.append({
            "model_name": "forecast_engine_v5",
            "rows": len(v5),
            "avg_confidence": round(pd.to_numeric(v5["confidence"], errors="coerce").fillna(0).mean(), 2),
            "learning_enabled": True,
            "model_type": "learning_baseline_hybrid",
        })

    if not baseline.empty:
        rows.append({
            "model_name": "learning_baseline_model_v1",
            "rows": len(baseline),
            "avg_confidence": round(pd.to_numeric(baseline["baseline_confidence"], errors="coerce").fillna(0).mean(), 2),
            "learning_enabled": True,
            "model_type": "historical_outcome_frequency_baseline",
        })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    best = out.sort_values(["learning_enabled", "avg_confidence", "rows"], ascending=[False, False, False]).iloc[0]

    REPORT.write_text(
        "\n".join([
            "# Model Comparison v1",
            "",
            f"Models compared: {len(out)}",
            f"Selected candidate: {best['model_name']}",
            "",
            "## CTO Assessment",
            "",
            "This comparison layer evaluates the available forecast models by coverage, confidence, and whether they use learned outcomes.",
            "It creates the basis for a production champion/challenger system.",
            "",
        ]),
        encoding="utf-8",
    )

    print("MODEL COMPARISON V1")
    print("===================")
    print(out)
    print(f"Selected candidate: {best['model_name']}")


if __name__ == "__main__":
    main()
