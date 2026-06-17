from collectors.providers.vast_real import VastRealProvider
import pandas as pd

provider = VastRealProvider()
rows = provider.fetch()

df = pd.DataFrame(rows)
df.to_csv("data/vast_live_report.csv", index=False)

print(f"Vast live rows: {len(df)}")
print(df.head() if not df.empty else "No live Vast data yet")
