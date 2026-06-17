import pandas as pd
from pathlib import Path

history_file = Path("data/live_gpu_price_history.csv")

if not history_file.exists():
    signal = "unknown"
    change_pct = 0
else:
    history = pd.read_csv(history_file)

    if len(history) < 2:
        signal = "insufficient_history"
        change_pct = 0
    else:
        latest = history.iloc[-1]["gpu_price_index"]
        previous = history.iloc[-2]["gpu_price_index"]

        change_pct = round(
            ((latest - previous) / previous) * 100,
            2
        )

        if change_pct > 5:
            signal = "price_pressure_up"
        elif change_pct < -5:
            signal = "price_pressure_down"
        else:
            signal = "stable"

out = pd.DataFrame([{
    "gpu_price_trend_signal": signal,
    "change_pct": change_pct
}])

out.to_csv(
    "data/gpu_price_trend_signal.csv",
    index=False
)

print(out)
