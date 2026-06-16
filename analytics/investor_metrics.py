import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv")

latest = rpct.iloc[-1]["score"]

result = pd.DataFrame([{
    "current_rpct": latest,
    "signal_strength": latest / 100,
    "market_temperature": latest
}])

result.to_csv(
    "data/investor_metrics.csv",
    index=False
)

print(result)
