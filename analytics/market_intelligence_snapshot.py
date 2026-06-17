import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

terminal = pd.read_csv("data/terminal_summary.csv").iloc[-1]
risk = pd.read_csv("data/terminal_risk_score.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]
share = pd.read_csv("data/live_provider_market_share.csv")

snapshot = f"""
AI-RPCT Market Intelligence Snapshot
Generated: {datetime.now()}

AI Infrastructure Index: {terminal['ai_infrastructure_index']}
GPU Price Index: {terminal['gpu_price_index']}
GPU Price Trend: {terminal['gpu_price_trend']}

Terminal Risk Score: {risk['terminal_risk_score']}
Risk Level: {risk['risk_level']}

Live Data Quality Score: {quality['live_data_quality_score']}

Live Provider Market Share:
{share.to_string(index=False)}
"""

filename = f"reports/market_intelligence_snapshot_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(snapshot)

print(snapshot)
