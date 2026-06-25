from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURE_STORE = Path("data/feature_store_v1.csv")
MODEL_SELECTION = Path("data/model_selection_v1.csv")

OUT = Path("data/forecast_engine_v4.csv")
REPORT = Path("reports/forecast_engine_v4.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def score_row(row) -> tuple[int, str]:
    score = 50

    # Market regime
    regime = str(row.get("market_regime", ""))

    if regime == "tight_market":
        score += 15
    elif regime == "balanced_market":
        score += 5
    elif regime == "oversupplied_market":
        score -= 10

    # Availability
    availability = float(row.get("availability_sum", 0))

    if availability < 2:
        score += 10
    elif availability > 25:
        score -= 5

    # Price spread
    spread = float(row.get("price_spread", 0))

    if spread > 0.30:
        score += 10

    # Historical context
    score += min(int(row.get("historical_gpu_release_count", 0)), 15) // 3
    score += min(int(row.get("historical_market_event_count", 0)), 10) // 2

    score = max(0, min(score, 100))

    if score >= 80:
        signal = "very_bullish"
    elif score >= 65:
        signal = "bullish"
    elif score >= 45:
        signal = "neutral"
    elif score >= 30:
        signal = "bearish"
    else:
        signal = "very_bearish"

    return score, signal


def main():
    features = read_csv(FEATURE_STORE)

    if features.empty:
        raise SystemExit("feature_store_v1.csv missing")

    selected = read_csv(MODEL_SELECTION)

    champion = (
        selected.iloc[0]["selected_model"]
        if not selected.empty
        else "unknown"
    )

    rows = []

    for _, row in features.iterrows():
        score, signal = score_row(row)

        rows.append({
            "provider": row.get("provider"),
            "gpu": row.get("gpu"),
            "forecast_score": score,
            "forecast_signal": signal,
            "market_regime": row.get("market_regime"),
            "champion_model": champion,
            "engine_version": "v4",
        })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    REPORT.write_text(
        f"""# Forecast Engine v4

Forecast rows: {len(out)}

Champion model:
{champion}

Forecast Engine v4 combines:

- Live provider features
- Market regime
- Historical GPU releases
- Historical market events
- Feature Store
- Champion model selection

This is the first multi-factor forecasting engine.
""",
        encoding="utf-8",
    )

    print("FORECAST ENGINE V4")
    print("==================")
    print(f"Rows: {len(out)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
