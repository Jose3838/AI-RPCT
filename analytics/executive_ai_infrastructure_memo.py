import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

risk = pd.read_csv("data/terminal_risk_score.csv").iloc[-1]
summary = pd.read_csv("data/terminal_summary.csv").iloc[-1]
frontier = pd.read_csv("data/frontier_gpu_index.csv").iloc[-1]
category = pd.read_csv("data/gpu_category_index.csv")

memo = f"""
AI-RPCT Executive AI Infrastructure Memo
Generated: {datetime.now()}

Overall Risk Level: {risk['risk_level']}
Terminal Risk Score: {risk['terminal_risk_score']}

AI Infrastructure Index: {summary['ai_infrastructure_index']}
GPU Price Index: {summary['gpu_price_index']}
GPU Price Trend: {summary['gpu_price_trend']}
Top Provider: {summary['top_provider']}

Frontier GPU Index: {frontier['frontier_gpu_index']}
Frontier Offers: {frontier['frontier_offers']}

GPU Category Index:
{category.to_string(index=False)}

Interpretation:
AI-RPCT monitors live GPU market data, provider health, pricing signals, scarcity indicators and infrastructure risk signals.
"""

filename = f"reports/executive_ai_infrastructure_memo_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(memo)

print(memo)
