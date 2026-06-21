import csv
import os
from datetime import datetime, timezone

import pandas as pd

FILE = "data/gpu_daily_state_history.csv"
SOURCE = "data/live_offers/provider_live_offer_history.csv"

def save_gpu_daily_state():

    df = pd.read_csv(SOURCE)

    exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not exists:

            writer.writerow([
                "timestamp",
                "gpu_model",
                "offers",
                "avg_price"
            ])

        for gpu in sorted(
            df["gpu_model"].dropna().unique()
        ):

            gpu_df = df[
                df["gpu_model"] == gpu
            ]

            writer.writerow([
                datetime.now(
                    timezone.utc
                ).isoformat(),
                gpu,
                len(gpu_df),
                round(
                    gpu_df[
                        "price_usd_per_gpu_hour"
                    ].astype(float).mean(),
                    4
                )
            ])

    return {
        "saved_gpus":
            df["gpu_model"]
            .nunique()
    }
