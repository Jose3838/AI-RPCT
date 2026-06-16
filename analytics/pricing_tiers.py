import pandas as pd

tiers = [
    {
        "tier": "starter",
        "price_usd_month": 49,
        "features": "dashboard, daily report"
    },
    {
        "tier": "pro",
        "price_usd_month": 299,
        "features": "dashboard, api, alerts, provider rankings"
    },
    {
        "tier": "enterprise",
        "price_usd_month": 2500,
        "features": "api, custom reports, white label, priority support"
    }
]

df = pd.DataFrame(tiers)
df.to_csv("data/pricing_tiers.csv", index=False)

print(df)
