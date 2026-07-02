from __future__ import annotations

from copilot.io import load_csv


def get_pricing_layer() -> dict:
    price_history = load_csv("data/gpu_price_history.csv")
    live_price_history = load_csv("data/live_gpu_price_history.csv")
    price_index = load_csv("data/live_gpu_price_index.csv")
    price_trend = load_csv("data/gpu_price_trend_signal.csv")
    price_volatility = load_csv("data/gpu_price_volatility.csv")

    return {
        "summary": {
            "gpu_price_history_records": len(price_history),
            "live_price_history_records": len(live_price_history),
            "price_index_records": len(price_index),
            "price_trend_records": len(price_trend),
            "price_volatility_records": len(price_volatility),
        },
        "gpu_price_history": price_history,
        "live_gpu_price_history": live_price_history,
        "live_gpu_price_index": price_index,
        "gpu_price_trend_signal": price_trend,
        "gpu_price_volatility": price_volatility,
    }
