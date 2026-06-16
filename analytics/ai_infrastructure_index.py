import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv").iloc[-1]
forecast = pd.read_csv("data/forecast_signal.csv").iloc[-1]
concentration = pd.read_csv("data/provider_concentration.csv").iloc[-1]

score = (
    float(rpct["score"]) * 0.4
    + float(forecast["forecast_score"]) * 0.4
    + min(float(concentration["hhi"]) / 100, 100) * 0.2
)

result = pd.DataFrame([{
    "ai_infrastructure_index": round(score, 2),
    "rpct_score": rpct["score"],
    "forecast_score": forecast["forecast_score"],
    "provider_hhi": concentration["hhi"]
}])

result.to_csv("data/ai_infrastructure_index.csv", index=False)

print(result)
