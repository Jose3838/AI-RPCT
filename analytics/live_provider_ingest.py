import pandas as pd
from pathlib import Path

from collectors.providers.vast_real import VastRealProvider

OUTPUT_COLUMNS = [
    "provider",
    "gpu",
    "price_per_hour",
    "availability",
    "timestamp"
]

providers = [
    VastRealProvider()
]

rows = []

for provider in providers:
    data = provider.fetch()
    rows.extend(data)

df = pd.DataFrame(rows)

Path("data").mkdir(exist_ok=True)

if df.empty:
    fallback = Path("data/vast_live_report.csv")
    if fallback.exists() and fallback.stat().st_size > 1:
        df = pd.read_csv(fallback)
        print("No fresh Vast rows; using last known Vast report.")
    else:
        df = pd.DataFrame(columns=OUTPUT_COLUMNS)

df.to_csv(
    "data/live_provider_data.csv",
    index=False
)

print(f"Live provider rows: {len(df)}")
print(df.head() if not df.empty else "No live provider data")
