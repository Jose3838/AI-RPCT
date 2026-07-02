import math

from fastapi import APIRouter

router = APIRouter()


def _json_safe(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


@router.get("/ai-index")
def ai_index():
    import pandas as pd

    return pd.read_csv(
        "data/ai_infrastructure_index.csv"
    ).to_dict(orient="records")


@router.get("/gpu-scarcity")
def gpu_scarcity():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_scarcity_index.csv"
    ).to_dict(orient="records")


@router.get("/ai-index-history")
def ai_index_history():
    import pandas as pd
    return pd.read_csv(
        "data/ai_infrastructure_index_history.csv"
    ).to_dict(orient="records")


@router.get("/index-history")
def index_history():
    import pandas as pd
    records = pd.read_csv("data/index_history.csv").to_dict(orient="records")
    return [
        {key: _json_safe(value) for key, value in row.items()}
        for row in records
    ]


@router.get("/gpu-price-index")
def gpu_price_index():
    import pandas as pd

    return pd.read_csv(
        "data/live_gpu_price_index.csv"
    ).to_dict(orient="records")


@router.get("/gpu-price-history")
def gpu_price_history():
    import pandas as pd
    return pd.read_csv("data/live_gpu_price_history.csv").to_dict(orient="records")


@router.get("/live-offer-summary")
def live_offer_summary():
    import pandas as pd
    return pd.read_csv("data/live_offer_summary.csv").to_dict(orient="records")


@router.get("/gpu-rankings")
def gpu_rankings():
    import pandas as pd

    return {
        "most_expensive": pd.read_csv(
            "data/live_gpu_most_expensive.csv"
        ).to_dict(orient="records"),
        "cheapest": pd.read_csv(
            "data/live_gpu_cheapest.csv"
        ).to_dict(orient="records"),
        "most_available": pd.read_csv(
            "data/live_gpu_most_available.csv"
        ).to_dict(orient="records")
    }


@router.get("/gpu-market-brief")
def gpu_market_brief():
    import pandas as pd
    return pd.read_csv(
        "data/gpu_market_brief.csv"
    ).to_dict(orient="records")


@router.get("/gpu-market-movers")
def gpu_market_movers():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_market_movers.csv"
    ).to_dict(orient="records")


@router.get("/live-gpu-alerts")
def live_gpu_alerts():
    import pandas as pd
    return pd.read_csv("data/live_gpu_alerts.csv").to_dict(orient="records")


@router.get("/gpu-price-trend")
def gpu_price_trend():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_price_trend_signal.csv"
    ).to_dict(orient="records")


@router.get("/gpu-watchlist")
def gpu_watchlist():
    import pandas as pd
    return pd.read_csv("data/gpu_watchlist_intelligence.csv").to_dict(orient="records")


@router.get("/frontier-gpu-index")
def frontier_gpu_index():
    import pandas as pd
    return pd.read_csv("data/frontier_gpu_index.csv").to_dict(orient="records")


@router.get("/gpu-category-index")
def gpu_category_index():
    import pandas as pd
    return pd.read_csv("data/gpu_category_index.csv").to_dict(orient="records")


@router.get("/scarcity-watchlist")
def scarcity_watchlist():
    import pandas as pd
    return pd.read_csv("data/scarcity_watchlist.csv").to_dict(orient="records")


@router.get("/gpu-price-volatility")
def gpu_price_volatility():
    import pandas as pd
    return pd.read_csv("data/gpu_price_volatility.csv").to_dict(orient="records")


@router.get("/ai-infrastructure-pulse")
def ai_infrastructure_pulse():
    import pandas as pd
    return pd.read_csv("data/ai_infrastructure_pulse.csv").to_dict(orient="records")
