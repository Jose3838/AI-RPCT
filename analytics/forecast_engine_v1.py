from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT = Path("data/forecast_features_v1.csv")
OUTPUT = Path("data/forecast_engine_v1.csv")
REPORT = Path("reports/forecast_engine_v1.md")


def read_features() -> pd.DataFrame:
    if not INPUT.exists() or INPUT.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(INPUT)


def classify_price_direction(row: pd.Series) -> str:
    spread = float(row.get("price_spread", 0) or 0)
    avg_price = float(row.get("avg_price", 0) or 0)

    if avg_price <= 0:
        return "insufficient_price_data"

    spread_ratio = spread / avg_price if avg_price else 0

    if spread_ratio >= 0.25:
        return "volatile_market"
    if spread_ratio >= 0.10:
        return "price_pressure_possible"
    return "stable_market"


def confidence_score(row: pd.Series) -> int:
    records = int(row.get("record_count", 0) or 0)
    availability = float(row.get("availability_sum", 0) or 0)

    score = 40

    if records >= 100:
        score += 25
    elif records >= 25:
        score += 15
    elif records >= 5:
        score += 5

    if availability >= 100:
        score += 20
    elif availability >= 25:
        score += 10
    elif availability > 0:
        score += 5

    return min(score, 95)


def recommendation(row: pd.Series, signal: str, confidence: int) -> str:
    if signal == "volatile_market" and confidence >= 70:
        return "Monitor closely before committing large GPU purchases."
    if signal == "price_pressure_possible" and confidence >= 60:
        return "Compare providers before committing capacity."
    if signal == "stable_market":
        return "Market appears stable for this provider/GPU pair."
    return "Collect more history before making forecast-backed decisions."


def main() -> None:
    df = read_features()

    rows = []
    for _, row in df.iterrows():
        signal = classify_price_direction(row)
        confidence = confidence_score(row)

        rows.append(
            {
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "forecast_signal": signal,
                "confidence": confidence,
                "avg_price": row.get("avg_price"),
                "price_spread": row.get("price_spread"),
                "record_count": row.get("record_count"),
                "availability_sum": row.get("availability_sum"),
                "recommendation": recommendation(row, signal, confidence),
            }
        )

    out = pd.DataFrame(rows)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUTPUT, index=False)

    high_confidence = int((out["confidence"] >= 70).sum()) if not out.empty else 0

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Engine v1",
                "",
                f"Forecast rows: {len(out)}",
                f"High-confidence rows: {high_confidence}",
                "",
                "## CTO Assessment",
                "",
                "Forecast Engine v1 is a rule-based predictive layer.",
                "It does not claim long-range prediction yet; it converts live market features into forecast signals and decision guidance.",
                "",
                "## Next Step",
                "",
                "Add backtesting once enough historical/live continuity exists.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V1")
    print("==================")
    print(f"Rows: {len(out)}")
    print(f"High confidence: {high_confidence}")
    print(f"CSV: {OUTPUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
