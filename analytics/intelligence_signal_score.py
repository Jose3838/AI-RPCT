import pandas as pd

terminal = pd.read_csv("data/terminal_summary.csv").iloc[-1]
health = pd.read_csv("data/provider_health.csv")
moat = pd.read_csv("data/market_data_moat_status.csv").iloc[-1]
frontier = pd.read_csv("data/frontier_gpu_index.csv").iloc[-1]

score = 0

if float(terminal["ai_infrastructure_index"]) >= 70:
    score += 25

if terminal["gpu_price_trend"] != "stable":
    score += 20

if health["health_score"].min() >= 80:
    score += 20

if float(moat["market_data_moat_score"]) >= 80:
    score += 20

if float(frontier["frontier_gpu_index"]) > 5:
    score += 15

signal = "high_attention" if score >= 70 else "normal_watch"

out = pd.DataFrame([{
    "intelligence_signal_score": score,
    "signal": signal
}])

out.to_csv("data/intelligence_signal_score.csv", index=False)

print(out)
