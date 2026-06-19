from pathlib import Path
import pandas as pd

FILES = [
    "data/live_offers/provider_live_offer_history.csv",
    "data/gpu_daily_state_history.csv",
    "data/provider_market_share_history.csv",
    "data/forecast_audit_history.csv",
    "data/feature_store/gpu_market_depth_history.csv",
]

def daily_data_health():

    result = []

    for file in FILES:

        path = Path(file)

        if not path.exists():

            result.append({
                "file": file,
                "exists": False,
                "rows": 0
            })

            continue

        try:
            df = pd.read_csv(path)
            rows = len(df)

        except Exception:
            rows = 0

        result.append({
            "file": file,
            "exists": True,
            "rows": rows,
            "size_bytes": path.stat().st_size
        })

    healthy = all(
        item["exists"]
        and item["rows"] > 0
        for item in result
    )

    return {
        "status": "healthy" if healthy else "incomplete",
        "assets": result
    }
