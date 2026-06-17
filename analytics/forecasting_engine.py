from pathlib import Path
import pandas as pd

DATA = Path("data")
DATA.mkdir(exist_ok=True)

history_path = DATA / "gpu_price_history.csv"
out_path = DATA / "gpu_price_forecast_signal.csv"

def write_signal(signal, trend, volatility=0, latest=None, previous=None, change_pct=None):
    df = pd.DataFrame([{
        "signal": signal,
        "trend": trend,
        "volatility": volatility,
        "latest_price_index": latest,
        "previous_price_index": previous,
        "change_pct": change_pct
    }])
    df.to_csv(out_path, index=False)

if not history_path.exists():
    write_signal("no_data", "unknown")
    print("no history data")
    raise SystemExit(0)

df = pd.read_csv(history_path)
price_col = "gpu_price_index"

if price_col not in df.columns:
    write_signal("missing_price_column", "unknown")
    print("missing gpu_price_index column")
    raise SystemExit(0)

df = df.dropna(subset=[price_col])

if len(df) < 2:
    latest = float(df[price_col].iloc[-1]) if len(df) == 1 else None
    write_signal("insufficient_data", "unknown", latest=latest)
    print("insufficient data")
    raise SystemExit(0)

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

write_signal(signal, trend, volatility, latest, previous, change_pct)
print("forecast signal generated")
