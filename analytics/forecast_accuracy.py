from __future__ import annotations

import pandas as pd


forecast = pd.read_csv("data/forecast_engine_v1_output.csv")
actual = pd.read_csv("data/rpct_scores.csv")

has_forecasts = len(forecast) > 0
has_actuals = len(actual) > 0

pd.DataFrame(
    [
        {
            "status": "not_applicable",
            "accuracy": "",
            "forecast_records": len(forecast),
            "actual_records": len(actual),
            "reason": (
                "Forecast engine v1 is rule-based and has no true labels. "
                "No production accuracy claim is made."
            ),
            "forecast_source": "data/forecast_engine_v1_output.csv",
            "actual_source": "data/rpct_scores.csv",
            "has_forecasts": has_forecasts,
            "has_actuals": has_actuals,
        }
    ]
).to_csv(
    "data/forecast_accuracy.csv",
    index=False,
)

print("Forecast accuracy: not applicable")
