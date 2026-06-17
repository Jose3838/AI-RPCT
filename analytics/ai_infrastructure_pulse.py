import pandas as pd

summary = pd.read_csv("data/terminal_summary.csv").iloc[-1]
risk = pd.read_csv("data/terminal_risk_score.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]
dominance = pd.read_csv("data/live_provider_dominance.csv").iloc[-1]
volatility = pd.read_csv("data/gpu_price_volatility.csv").iloc[-1]

pulse_score = 0

pulse_score += min(float(summary["ai_infrastructure_index"]), 30)
pulse_score += min(float(risk["terminal_risk_score"]), 25)
pulse_score += 20 if float(quality["live_data_quality_score"]) >= 90 else 10
pulse_score += 15 if float(dominance["dominance_pct"]) >= 60 else 5
pulse_score += 10 if float(volatility["gpu_price_volatility"]) > 0 else 0

pulse_score = round(min(pulse_score, 100), 2)

out = pd.DataFrame([{
    "ai_infrastructure_pulse": pulse_score,
    "risk_level": risk["risk_level"],
    "dominant_provider": dominance["dominant_provider"],
    "gpu_price_trend": summary["gpu_price_trend"]
}])

out.to_csv("data/ai_infrastructure_pulse.csv", index=False)

print(out)
