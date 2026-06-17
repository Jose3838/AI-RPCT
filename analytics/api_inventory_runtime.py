import pandas as pd

endpoints = [
    "/",
    "/health",
    "/terminal",
    "/terminal-summary",
    "/terminal-kpis",
    "/provider-health",
    "/provider-reliability",
    "/provider-comparison",
    "/gpu-price-index",
    "/gpu-price-history",
    "/gpu-price-trend",
    "/gpu-rankings",
    "/gpu-market-brief",
    "/live-gpu-alerts",
    "/weekly-infrastructure-report",
    "/runpod-live-report",
    "/vast-live-report",
    "/public-status"
]

df = pd.DataFrame([
    {"endpoint": e, "status": "active"}
    for e in endpoints
])

df.to_csv("data/api_inventory_runtime.csv", index=False)

print(df)
