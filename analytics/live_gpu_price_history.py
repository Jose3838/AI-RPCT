import pandas as pd
from pathlib import Path
from datetime import datetime

current = pd.read_csv("data/live_gpu_price_index.csv")
current["date"] = datetime.now().strftime("%Y-%m-%d")
current["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

history_file = "data/live_gpu_price_history.csv"

if Path(history_file).exists():
    old = pd.read_csv(history_file)
    out = pd.concat([old, current], ignore_index=True)
else:
    out = current

out.to_csv(history_file, index=False)

print(out.tail())
