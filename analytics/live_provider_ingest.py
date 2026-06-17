import pandas as pd
from pathlib import Path

from collectors.providers.vast_real import VastRealProvider

providers = [
    VastRealProvider()
]

rows = []

for provider in providers:
    data = provider.fetch()
    rows.extend(data)

df = pd.DataFrame(rows)

Path("data").mkdir(exist_ok=True)

df.to_csv(
    "data/live_provider_data.csv",
    index=False
)

print(f"Live provider rows: {len(df)}")
print(df.head() if not df.empty else "No live provider data")
