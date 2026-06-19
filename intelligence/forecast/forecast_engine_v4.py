import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def forecast_engine_v4():

    df = pd.read_csv(FILE)

    forecasts = []

    for gpu in df["gpu_model"].dropna().unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        if len(gpu_df) < 5:
            continue

        prices = gpu_df[
            "price_usd_per_gpu_hour"
        ].astype(float)

        recent = prices.tail(5).mean()
        historical = prices.mean()

        if recent > historical * 1.05:
            signal = "bullish"

        elif recent < historical * 0.95:
            signal = "bearish"

        else:
            signal = "neutral"

        forecasts.append({
            "gpu_model": gpu,
            "signal": signal,
            "recent_price":
                round(recent, 4),
            "historical_price":
                round(historical, 4)
        })

    return forecasts
