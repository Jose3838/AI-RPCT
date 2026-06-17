import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

pulse = pd.read_csv("data/ai_infrastructure_pulse.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]
moat = pd.read_csv("data/market_data_moat_status.csv").iloc[-1]
share = pd.read_csv("data/live_provider_market_share.csv")

text = f"""
AI-RPCT Investor Snapshot
Generated: {datetime.now()}

AI Infrastructure Pulse: {pulse['ai_infrastructure_pulse']}
Risk Level: {pulse['risk_level']}
Dominant Provider: {pulse['dominant_provider']}
GPU Price Trend: {pulse['gpu_price_trend']}

Live Data Quality: {quality['live_data_quality_score']}
Market Data Moat Score: {moat['market_data_moat_score']}

Provider Market Share:
{share.to_string(index=False)}
"""

filename = f"reports/investor_snapshot_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(text)

print(text)
