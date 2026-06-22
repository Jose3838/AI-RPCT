import pandas as pd
from pathlib import Path

path = Path("data/live_provider_data.csv")

if path.exists() and path.stat().st_size > 1:
    df = pd.read_csv(path)
else:
    df = pd.DataFrame(columns=["price_per_hour"])

price_index = round(
    df["price_per_hour"].mean() if not df.empty else 0,
    4
)

out = pd.DataFrame([{
    "gpu_price_index": price_index,
    "offers": len(df)
}])

out.to_csv(
    "data/live_gpu_price_index.csv",
    index=False
)

print(out)
