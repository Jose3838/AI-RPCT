import pandas as pd
from pathlib import Path

history_file = "data/live_gpu_price_history.csv"

if not Path(history_file).exists():
    print("No history available.")
    raise SystemExit(0)

history = pd.read_csv(history_file)

if len(history) < 2:
    print("Need at least 2 observations.")
    raise SystemExit(0)

latest = history.iloc[-1]
previous = history.iloc[-2]

change = latest["gpu_price_index"] - previous["gpu_price_index"]

out = pd.DataFrame([{
    "current_gpu_price_index": round(latest["gpu_price_index"], 4),
    "previous_gpu_price_index": round(previous["gpu_price_index"], 4),
    "change": round(change, 4),
    "change_pct": round(
        (change / previous["gpu_price_index"]) * 100,
        2
    )
}])

out.to_csv(
    "data/gpu_market_movers.csv",
    index=False
)

print(out)
