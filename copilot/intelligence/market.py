from __future__ import annotations

from copilot.io import load_csv


def get_market_layer() -> dict:
    market_brief = load_csv("data/gpu_market_brief.csv")
    market_movers = load_csv("data/gpu_market_movers.csv")
    frontier_index = load_csv("data/frontier_gpu_index.csv")
    category_index = load_csv("data/gpu_category_index.csv")
    watchlist = load_csv("data/gpu_watchlist_intelligence.csv")

    return {
        "summary": {
            "market_brief_records": len(market_brief),
            "market_mover_records": len(market_movers),
            "frontier_index_records": len(frontier_index),
            "category_index_records": len(category_index),
            "watchlist_records": len(watchlist),
        },
        "gpu_market_brief": market_brief,
        "gpu_market_movers": market_movers,
        "frontier_gpu_index": frontier_index,
        "gpu_category_index": category_index,
        "gpu_watchlist_intelligence": watchlist,
    }
