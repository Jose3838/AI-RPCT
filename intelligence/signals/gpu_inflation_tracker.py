import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_inflation_tracker():

    df = pd.read_csv(FILE)

    results = []

    for gpu in df["gpu_model"].dropna().unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        gpu_df = gpu_df.sort_values(
            "observed_at"
        )

        if len(gpu_df) < 2:
            continue

        first_price = pd.to_numeric(
            gpu_df.iloc[0]["price_usd_per_gpu_hour"],
            errors="coerce"
        )

        last_price = pd.to_numeric(
            gpu_df.iloc[-1]["price_usd_per_gpu_hour"],
            errors="coerce"
        )

        if pd.isna(first_price) or pd.isna(last_price):
            continue

        inflation = (
            (last_price - first_price)
            / first_price
        ) * 100

        results.append({
            "gpu_model": gpu,
            "price_change_pct": round(
                inflation,
                2
            )
        })

    return sorted(
        results,
        key=lambda x:x["price_change_pct"],
        reverse=True
    )
