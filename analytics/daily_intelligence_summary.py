import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

ai_index = pd.read_csv("data/ai_infrastructure_index.csv").iloc[-1]
gpu_scarcity = pd.read_csv("data/gpu_scarcity_index.csv").iloc[-1]
dominance = pd.read_csv("data/provider_dominance_index.csv").iloc[-1]
data_moat = pd.read_csv("data/data_moat_score.csv").iloc[-1]

summary = f"""
AI-RPCT Daily Intelligence Summary
Generated: {datetime.now()}

AI Infrastructure Index: {ai_index['ai_infrastructure_index']}
GPU Scarcity Index: {gpu_scarcity['gpu_scarcity_index']}
Provider Dominance Index: {dominance['provider_dominance_index']}
Data Moat Score: {data_moat['data_moat_score']}%

Interpretation:
This report summarizes the current AI infrastructure pressure, GPU scarcity, provider dominance, and historical data moat strength.
"""

filename = f"reports/daily_intelligence_summary_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(summary)

print(summary)
print(f"Saved: {filename}")
