from pathlib import Path

def dataset_growth():

    p = Path(
        "data/live_offers/provider_live_offer_history.csv"
    )

    if not p.exists():
        return {
            "size_bytes": 0
        }

    return {
        "size_bytes": p.stat().st_size
    }
