from __future__ import annotations

from pathlib import Path
import pandas as pd

INPUT = Path("warehouse/provider_timeseries")
OUT = Path("data/forecast_engine_v2.csv")
REPORT = Path("reports/forecast_engine_v2.md")

def load_timeseries():
    frames = []
    for path in INPUT.rglob("*.csv"):
        df = pd.read_csv(path)
        df["source_file"] = path.name
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()

def signal(row):
    if row["price_trend"] > 0.05:
        return "price_increase_likely"
    if row["price_trend"] < -0.05:
        return "price_decrease_likely"
    if row["availability_trend"] < -0.10:
        return "availability_tightening"
    return "stable_market_expected"

def main():
    df = load_timeseries()
    if df.empty:
        raise SystemExit("No provider timeseries found")

    df["price_per_hour"] = pd.to_numeric(df["price_per_hour"], errors="coerce").fillna(0)
    df["availability"] = pd.to_numeric(df["availability"], errors="coerce").fillna(0)

    rows = []
    for (provider, gpu), g in df.groupby(["provider", "gpu"], dropna=False):
        g = g.reset_index(drop=True)
        first_price = float(g["price_per_hour"].iloc[0])
        last_price = float(g["price_per_hour"].iloc[-1])
        first_avail = float(g["availability"].iloc[0])
        last_avail = float(g["availability"].iloc[-1])

        price_trend = ((last_price - first_price) / first_price) if first_price else 0
        availability_trend = ((last_avail - first_avail) / first_avail) if first_avail else 0
        record_count = len(g)

        rows.append({
            "model_name": "forecast_engine_v2",
            "provider": provider,
            "gpu": gpu,
            "record_count": record_count,
            "avg_price": round(g["price_per_hour"].mean(), 4),
            "price_trend": round(price_trend, 4),
            "availability_trend": round(availability_trend, 4),
            "forecast_signal": signal({
                "price_trend": price_trend,
                "availability_trend": availability_trend,
            }),
            "confidence": min(95, 50 + min(record_count, 45)),
        })

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)
    out.to_csv(OUT, index=False)

    REPORT.write_text(
        f"# Forecast Engine v2\n\nRows: {len(out)}\n\nv2 uses observed provider time-series trends instead of only rule-based current-state features.\n",
        encoding="utf-8",
    )

    print("FORECAST ENGINE V2")
    print("==================")
    print(f"Rows: {len(out)}")
    print(f"CSV: {OUT}")

if __name__ == "__main__":
    main()
