import json
import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv").iloc[-1]
forecast = pd.read_csv("data/forecast_signal.csv").iloc[-1]

payload = {
    "rpct_score": float(rpct["score"]),
    "regime": str(rpct["regime"]),
    "forecast_score": float(forecast["forecast_score"]),
    "outlook": str(forecast["outlook"])
}

with open("data/api_metrics.json", "w") as f:
    json.dump(payload, f, indent=2)

print(json.dumps(payload, indent=2))
