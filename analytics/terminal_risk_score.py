import pandas as pd

signal = pd.read_csv("data/intelligence_signal_score.csv").iloc[-1]
scarcity = pd.read_csv("data/scarcity_watchlist.csv")
health = pd.read_csv("data/provider_health.csv")
trend = pd.read_csv("data/gpu_price_trend_signal.csv").iloc[-1]

risk = 0

risk += min(float(signal["intelligence_signal_score"]), 40)

if len(scarcity) > 0:
    risk += min(len(scarcity) * 5, 25)

if health["health_score"].min() < 100:
    risk += 15

if trend["gpu_price_trend_signal"] != "stable":
    risk += 20

risk = min(risk, 100)

level = "high" if risk >= 70 else "medium" if risk >= 40 else "low"

out = pd.DataFrame([{
    "terminal_risk_score": risk,
    "risk_level": level
}])

out.to_csv("data/terminal_risk_score.csv", index=False)

print(out)
