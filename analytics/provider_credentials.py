import os
import pandas as pd

keys = {
    "runpod": os.getenv("RUNPOD_API_KEY"),
    "vast": os.getenv("VAST_API_KEY"),
    "lambda": os.getenv("LAMBDA_API_KEY"),
    "coreweave": os.getenv("COREWEAVE_API_KEY")
}

rows = []

for provider, key in keys.items():
    rows.append({
        "provider": provider,
        "configured": bool(key)
    })

df = pd.DataFrame(rows)
df.to_csv("data/provider_credentials.csv", index=False)

print(df)
