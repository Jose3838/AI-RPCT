import pandas as pd
from pathlib import Path

history_file = Path("data/live_gpu_price_history.csv")

if not history_file.exists():
    out = pd.DataFrame([{
        "gpu_price_volatility": 0,
        "observations": 0
    }])
else:
    history = pd.read_csv(history_file)

    volatility = round(
        history["gpu_price_index"].std(),
        4
    ) if len(history) > 1 else 0

    out = pd.DataFrame([{
        "gpu_price_volatility": volatility,
        "observations": len(history)
    }])

out.to_csv("data/gpu_price_volatility.csv", index=False)

print(out)
