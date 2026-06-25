# Forecasting Pipeline

## Current Forecast Flow

1. Live and historical data are collected.
2. Feature Store v2 enriches provider/GPU features.
3. Forecast Engine v9 creates explainable forecast signals.
4. Forecast snapshots are stored.
5. Outcome windows are created.
6. Maturity monitor waits for future dates.
7. Resolver creates trainable labels only after future observations exist.
8. Training Dataset v3 blocks ML training until true labels are available.

## Current Forecast Status

Forecasts are suitable for customer preview language only.

Allowed claim:

"Early directional forecast preview based on historical and live infrastructure signals."

Blocked claim:

"Validated predictive AI with guaranteed forecasting performance."
