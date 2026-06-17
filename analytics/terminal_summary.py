import pandas as pd

summary = {}

try:
    summary["ai_infrastructure_index"] = pd.read_csv(
        "data/ai_infrastructure_index.csv"
    ).iloc[-1]["ai_infrastructure_index"]
except:
    summary["ai_infrastructure_index"] = None

try:
    summary["gpu_price_index"] = pd.read_csv(
        "data/live_gpu_price_index.csv"
    ).iloc[-1]["gpu_price_index"]
except:
    summary["gpu_price_index"] = None

try:
    summary["gpu_price_trend"] = pd.read_csv(
        "data/gpu_price_trend_signal.csv"
    ).iloc[-1]["gpu_price_trend_signal"]
except:
    summary["gpu_price_trend"] = None

try:
    summary["top_provider"] = pd.read_csv(
        "data/provider_reliability_ranking.csv"
    ).iloc[0]["provider"]
except:
    summary["top_provider"] = None

try:
    summary["active_alerts"] = len(pd.read_csv(
        "data/live_gpu_alerts.csv"
    ))
except:
    summary["active_alerts"] = None

pd.DataFrame([summary]).to_csv(
    "data/terminal_summary.csv",
    index=False
)

print(summary)
