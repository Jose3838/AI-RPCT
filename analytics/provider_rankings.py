import pandas as pd

df = pd.read_csv("data/gpu_data.csv")

provider_scores = (
    df.groupby("provider")
      .agg({
          "price_per_hour": "mean",
          "availability": "mean"
      })
      .reset_index()
)

provider_scores["score"] = (
    (provider_scores["availability"] / provider_scores["availability"].max()) * 50
    +
    ((provider_scores["price_per_hour"].max() - provider_scores["price_per_hour"])
     / provider_scores["price_per_hour"].max()) * 50
)

provider_scores = provider_scores.sort_values(
    "score",
    ascending=False
)

provider_scores.to_csv(
    "data/provider_rankings.csv",
    index=False
)

print(provider_scores)
