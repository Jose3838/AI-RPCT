from pathlib import Path
import pandas as pd

DATA = Path("data")

history_path = DATA / "gpu_price_history.csv"
out_path = DATA / "gpu_price_forecast_signal.csv"

if not history_path.exists():
    pd.DataFrame([{
        "signal": "no_data",
        "trend": "unknown",
        "volatility": 0,
        "latest_price_index": None,
        "previous_price_index": None,
        "change_pct": None
    }]).to_csv(out_path, index=False)
    print("no history data")
    raise SystemExit

df = pd.read_csv(history_path)

price_col = "gpu_price_index"

if price_col not in df.columns or len(df) < 2:
    pd.DataFrame([{
        "signal": "insufficient_data",
        "trend": "unknown",
        "volatility": 0,
        "latest_price_index": None,
        "previous_price_index": None,
        "change_pct": None
    }]).to_csv(out_path, index=False)
    print("insufficient data")
    raise SystemExit

df = df.dropna(subset=[price_col])
latest = float(df[price_col].iloc[-1])
previous = float(df[price_col].iloc[-2])

change_pct = round(((latest - previous) / previous) * 100, 2) if previous else 0
volatility = round(float(df[price_col].tail(20).std()), 4)

if change_pct > 5:
    trend = "price_spike"
    signal = "watch"
elif change_pct < -5:
    trend = "price_drop"
    signal = "opportunity"
else:
    trend = "stable"
    signal = "normal"

pd.DataFrame([{
    "signal": signal,
    "trend": trend,
    "volatility": volatility,
    "latest_price_index": latest,
    "previous_price_index": previous,
    "change_pct": change_pct
}]).to_csv(out_path, index=False)

print("forecast signal generated")
print(pd.read_csv(out_path).to_string(index=False))
