import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_opportunity_ranking_v1():

    df = pd.read_csv(FILE)

    opportunities = []

    for gpu in df["gpu_model"].dropna().unique():

        gpu_df = df[df["gpu_model"] == gpu]

        if len(gpu_df) < 5:
            continue

        prices = gpu_df[
            "price_usd_per_gpu_hour"
        ].astype(float)

        avg_price = prices.mean()
        min_price = prices.min()

        discount = (
            (avg_price - min_price)
            / avg_price
            * 100
        )

        opportunities.append({
            "gpu_model": gpu,
            "avg_price": round(avg_price, 4),
            "best_price": round(min_price, 4),
            "discount_pct": round(discount, 2)
        })

    opportunities.sort(
        key=lambda x: x["discount_pct"],
        reverse=True
    )

    return opportunities[:10]
