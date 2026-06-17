import pandas as pd

df = pd.read_csv("data/provider_health.csv")

ranking = df.sort_values(
    ["health_score", "rows"],
    ascending=False
)

ranking.to_csv(
    "data/provider_reliability_ranking.csv",
    index=False
)

print(ranking)
