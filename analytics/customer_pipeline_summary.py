import pandas as pd
from pathlib import Path

path = Path("data/customer_pipeline.csv")

if path.exists():
    df = pd.read_csv(path)
    total = len(df)
else:
    total = 0

out = pd.DataFrame([{
    "pipeline_contacts": total,
    "status": "empty" if total == 0 else "active"
}])

out.to_csv("data/customer_pipeline_summary.csv", index=False)

print(out)
