from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT = Path("data/forecast_features_v1.csv")
OUTPUT = Path("data/market_regime_v1.csv")
REPORT = Path("reports/market_regime_v1.md")


def classify(row):
    availability = float(row.get("availability_sum", 0) or 0)
    spread = float(row.get("price_spread", 0) or 0)

    if availability < 10 and spread > 0.50:
        return "capacity_crunch"
    if availability < 20:
        return "tight_market"
    if spread > 0.30:
        return "volatile_market"
    if availability > 100:
        return "oversupply"
    return "stable_market"


def confidence(row):
    records = int(row.get("record_count", 0) or 0)
    if records > 100:
        return 90
    if records > 50:
        return 80
    if records > 20:
        return 70
    return 60


def main():
    df = pd.read_csv(INPUT)
    rows = []

    for _, row in df.iterrows():
        rows.append({
            "provider": row["provider"],
            "gpu": row["gpu"],
            "market_regime": classify(row),
            "confidence": confidence(row),
            "records": row["record_count"],
            "avg_price": row["avg_price"],
            "availability_sum": row["availability_sum"],
            "price_spread": row["price_spread"],
        })

    out = pd.DataFrame(rows)
    OUTPUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)
    out.to_csv(OUTPUT, index=False)

    REPORT.write_text(
        f"""# Market Regime Detector v1

Regimes detected: {len(out)}

This module classifies the current provider/GPU market state.

Regimes:
- stable_market
- tight_market
- capacity_crunch
- volatile_market
- oversupply
""",
        encoding="utf-8",
    )

    print("MARKET REGIME DETECTOR V1")
    print("=========================")
    print(f"Rows: {len(out)}")
    print(f"CSV: {OUTPUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
