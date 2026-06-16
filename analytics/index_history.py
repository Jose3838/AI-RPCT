import pandas as pd
from pathlib import Path
from datetime import datetime

files = {
    "ai_infrastructure": "data/ai_infrastructure_index.csv",
    "gpu_scarcity": "data/gpu_scarcity_index.csv",
    "provider_concentration": "data/provider_concentration.csv"
}

rows = []

for name, path in files.items():
    if Path(path).exists():
        df = pd.read_csv(path).iloc[-1].to_dict()
        df["index_name"] = name
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        rows.append(df)

out = pd.DataFrame(rows)

history_file = "data/index_history.csv"

if Path(history_file).exists():
    old = pd.read_csv(history_file)
    out = pd.concat([old, out], ignore_index=True)

out.to_csv(history_file, index=False)

print(out.tail())
