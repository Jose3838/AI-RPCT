import pandas as pd

alerts = []

try:
    df = pd.read_csv(
        "data/provider_marketshare.csv"
    )

    top = df.sort_values(
        "market_share",
        ascending=False
    ).iloc[0]

    if top["market_share"] > 50:
        alerts.append(
            f"Provider concentration risk: {top['provider']}"
        )

except Exception as e:
    alerts.append(str(e))

pd.DataFrame(
    {"alert": alerts}
).to_csv(
    "data/alerts.csv",
    index=False
)

print(alerts)
