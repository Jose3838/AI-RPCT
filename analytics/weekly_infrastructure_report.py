import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

ai_index = pd.read_csv("data/ai_infrastructure_index.csv").iloc[-1]
gpu_price = pd.read_csv("data/live_gpu_price_index.csv").iloc[-1]
brief = pd.read_csv("data/gpu_market_brief.csv").iloc[-1]
alerts = pd.read_csv("data/live_gpu_alerts.csv")

report = f"""
AI-RPCT Weekly Infrastructure Report
Generated: {datetime.now()}

AI Infrastructure Index: {ai_index['ai_infrastructure_index']}
GPU Price Index: {gpu_price['gpu_price_index']}
Offers Tracked: {gpu_price['offers']}

Most Expensive GPU: {brief['most_expensive_gpu']}
Highest Avg Price: {brief['highest_avg_price']}
Most Available GPU: {brief['most_available_gpu']}
Highest Offer Count: {brief['highest_offer_count']}

Alerts:
{alerts.to_string(index=False)}
"""

filename = f"reports/weekly_infrastructure_report_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(report)

print(report)
