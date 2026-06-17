import pandas as pd
from pathlib import Path
from datetime import datetime

rows = []

providers = [
    ("vast", "data/live_provider_data.csv"),
    ("runpod", "data/runpod_live_report.csv")
]

for provider, file_path in providers:

    status = "offline"
    rows_count = 0
    freshness_hours = None
    health_score = 0

    path = Path(file_path)

    if path.exists():

        try:
            df = pd.read_csv(path)

            rows_count = len(df)

            if rows_count > 0:
                status = "online"
                health_score += 50

            if "timestamp" in df.columns:

                latest = pd.to_datetime(df["timestamp"]).max()

                freshness_hours = round(
                    (datetime.now() - latest).total_seconds() / 3600,
                    2
                )

                if freshness_hours < 24:
                    health_score += 50

        except Exception:
            pass

    rows.append({
        "provider": provider,
        "status": status,
        "rows": rows_count,
        "freshness_hours": freshness_hours,
        "health_score": health_score
    })

pd.DataFrame(rows).to_csv(
    "data/provider_health.csv",
    index=False
)

print(pd.DataFrame(rows))
