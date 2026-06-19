import pandas as pd

FILE = "data/feature_store/gpu_market_depth_history.csv"

def gpu_price_trend():

    df = pd.read_csv(FILE)

    if len(df) < 2:
        return []

    results = []

    for gpu in df["gpu_model"].unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ].copy()

        if len(gpu_df) < 2:
            continue

        latest = gpu_df.iloc[-1]
        previous = gpu_df.iloc[-2]

        delta = (
            float(latest["avg_price"])
            -
            float(previous["avg_price"])
        )

        results.append({
            "gpu_model": gpu,
            "price_change": round(delta, 4)
        })

    return sorted(
        results,
        key=lambda x: abs(x["price_change"]),
        reverse=True
    )
