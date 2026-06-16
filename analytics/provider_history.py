import pandas as pd

df = pd.read_csv(
    "data/provider_rankings.csv"
)

summary = df.groupby(
    "provider"
).mean(
    numeric_only=True
)

summary.to_csv(
    "data/provider_history.csv"
)

print(summary)
