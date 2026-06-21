import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"


def gpu_risk_advisor_v1():

    df = pd.read_csv(FILE)

    risks = []

    for gpu in df["gpu_model"].dropna().unique():

        gpu_df = df[df["gpu_model"] == gpu]

        if len(gpu_df) < 5:
            continue

        prices = gpu_df["price_usd_per_gpu_hour"].astype(float)

        avg_price = prices.mean()
        latest_price = prices.tail(5).mean()
        min_price = prices.min()

        premium_pct = (
            (latest_price - avg_price)
            / avg_price
            * 100
        )

        spread_pct = (
            (avg_price - min_price)
            / avg_price
            * 100
        )

        if premium_pct >= 20:
            risk = "high_price_risk"
            action = "avoid_now"
        elif premium_pct >= 5:
            risk = "moderate_price_risk"
            action = "wait"
        elif spread_pct >= 25:
            risk = "price_fragmentation"
            action = "compare_providers"
        else:
            risk = "low_risk"
            action = "normal"

        risks.append({
            "gpu_model": gpu,
            "risk": risk,
            "recommended_action": action,
            "avg_price": round(avg_price, 4),
            "latest_price": round(latest_price, 4),
            "premium_pct": round(premium_pct, 2),
            "spread_pct": round(spread_pct, 2),
            "observations": int(len(gpu_df))
        })

    risks.sort(
        key=lambda x: (
            x["risk"] != "high_price_risk",
            x["risk"] != "moderate_price_risk",
            -x["premium_pct"]
        )
    )

    return {
        "status": "ok",
        "version": "v1",
        "risks": risks[:20]
    }
