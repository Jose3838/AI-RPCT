import pandas as pd
from pathlib import Path

endpoints = [
    "/rpct",
    "/forecast",
    "/providers",
    "/marketshare",
    "/concentration",
    "/alerts",
    "/data-quality"
]

df = pd.DataFrame([{
    "endpoint": e,
    "status": "active"
} for e in endpoints])

Path("data").mkdir(exist_ok=True)
df.to_csv("data/usage_metrics.csv", index=False)

print(df)
