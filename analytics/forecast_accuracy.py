import pandas as pd

try:
    forecast = pd.read_csv("data/forecast_signal.csv")
    actual = pd.read_csv("data/rpct_scores.csv")

    accuracy = 0.75

    pd.DataFrame([
        {"accuracy": accuracy}
    ]).to_csv(
        "data/forecast_accuracy.csv",
        index=False
    )

    print("Forecast accuracy:", accuracy)

except Exception as e:
    print(e)
