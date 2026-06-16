import pandas as pd

df = pd.read_csv("data/rpct_scores.csv")

window = min(7, len(df))

forecast = df["score"].tail(window).mean()

result = pd.DataFrame([
    {
        "forecast_score": round(forecast, 2)
    }
])

result.to_csv(
    "data/time_series_forecast.csv",
    index=False
)

print(result)
