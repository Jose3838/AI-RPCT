import os
import pandas as pd

providers = [
    {
        "provider": "vast",
        "env_key": "VAST_API_KEY",
        "configured": bool(
            os.getenv("VAST_API_KEY")
        )
    },
    {
        "provider": "runpod",
        "env_key": "RUNPOD_API_KEY",
        "configured": bool(
            os.getenv("RUNPOD_API_KEY")
        )
    }
]

df = pd.DataFrame(providers)

df.to_csv(
    "data/provider_live_readiness.csv",
    index=False
)

print(df)
