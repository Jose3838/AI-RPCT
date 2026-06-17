import os
import pandas as pd
from datetime import datetime

providers = [
    {"provider": "vast", "env_key": "VAST_API_KEY"},
    {"provider": "runpod", "env_key": "RUNPOD_API_KEY"},
    {"provider": "lambda", "env_key": "LAMBDA_API_KEY"},
    {"provider": "coreweave", "env_key": "COREWEAVE_API_KEY"}
]

rows = []

for p in providers:
    rows.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": p["provider"],
        "env_key": p["env_key"],
        "configured": bool(os.getenv(p["env_key"]))
    })

df = pd.DataFrame(rows)
df.to_csv("data/live_provider_status.csv", index=False)

print(df)
