import pandas as pd
from datetime import datetime

rpct = pd.read_csv("data/rpct_scores.csv").iloc[-1]
forecast = pd.read_csv("data/forecast_signal.csv").iloc[-1]
providers = pd.read_csv("data/provider_rankings.csv")

report = f"""
AI-RPCT DAILY REPORT
====================

Generated:
{datetime.now()}

Current RPCT Score:
{rpct['score']}

Regime:
{rpct['regime']}

Forecast Score:
{forecast['forecast_score']:.2f}

Outlook:
{forecast['outlook']}

Top Providers:
"""

for _, row in providers.head(5).iterrows():
    report += f"\n{row['provider']} | Score={row['score']:.2f}"

filename = f"reports/report_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(report)

print(report)
print(f"\nSaved: {filename}")
