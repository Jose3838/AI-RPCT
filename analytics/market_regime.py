import pandas as pd

score = pd.read_csv(
    "data/rpct_scores.csv"
).iloc[-1]["score"]

if score >= 80:
    regime = "GPU_BULL"
elif score >= 60:
    regime = "NEUTRAL"
else:
    regime = "GPU_BEAR"

pd.DataFrame([
    {
        "regime": regime,
        "score": score
    }
]).to_csv(
    "data/market_regime.csv",
    index=False
)

print(regime)
