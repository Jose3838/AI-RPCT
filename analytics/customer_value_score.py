import pandas as pd

pulse = pd.read_csv("data/ai_infrastructure_pulse.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]
moat = pd.read_csv("data/market_data_moat_status.csv").iloc[-1]
providers = pd.read_csv("data/provider_health.csv")

score = 0

if float(pulse["ai_infrastructure_pulse"]) > 50:
    score += 30

if float(quality["live_data_quality_score"]) >= 90:
    score += 25

if float(moat["market_data_moat_score"]) >= 80:
    score += 25

if len(providers[providers["status"] == "online"]) >= 2:
    score += 20

out = pd.DataFrame([{
    "customer_value_score": score,
    "positioning": "high_value_beta" if score >= 80 else "early_beta"
}])

out.to_csv("data/customer_value_score.csv", index=False)

print(out)
