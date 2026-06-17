import pandas as pd
from datetime import datetime

endpoints = [
    "/web",
    "/terminal-summary",
    "/gpu-rankings",
    "/provider-health",
    "/live-provider-market-share",
    "/weekly-infrastructure-report",
    "/investor-snapshot"
]

df = pd.DataFrame([{
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "tracked_public_endpoints": len(endpoints),
    "important_endpoints": ", ".join(endpoints)
}])

df.to_csv("data/public_usage_snapshot.csv", index=False)

print(df)
