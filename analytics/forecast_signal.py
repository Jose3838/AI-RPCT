import pandas as pd
from pathlib import Path

rpct = pd.read_csv("data/rpct_scores.csv")
shortage = pd.read_csv("data/shortage_probability.csv").iloc[-1]

latest_score = float(rpct.iloc[-1]["score"])
shortage_probability = float(shortage["shortage_probability"])

forecast_score = (latest_score * 0.6) + (shortage_probability * 0.4)

if forecast_score < 40:
    outlook = "LOW RISK"
elif forecast_score < 70:
    outlook = "ELEVATED RISK"
else:
    outlook = "HIGH RISK"

result = pd.DataFrame([{
    "latest_rpct": latest_score,
    "shortage_probability": shortage_probability,
    "forecast_score": forecast_score,
    "outlook": outlook
}])

result.to_csv("data/forecast_signal.csv", index=False)

print(result)
