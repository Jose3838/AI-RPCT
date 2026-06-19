import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def calculate_gpu_scarcity():

    df = pd.read_csv(FILE)

    latest_ts = df["observed_at"].max()

    latest = df[df["observed_at"] == latest_ts]

    results = []

    for gpu in latest["gpu_model"].dropna().unique():

        gpu_df = latest[
            latest["gpu_model"] == gpu
        ]

        total = len(gpu_df)

        available = gpu_df["available"].astype(bool).sum()

        scarcity = 1 - (
            available / max(total,1)
        )

        results.append({
            "gpu_model": gpu,
            "scarcity_index": round(scarcity,4),
            "offers": total
        })

    return sorted(
        results,
        key=lambda x:x["scarcity_index"],
        reverse=True
    )
