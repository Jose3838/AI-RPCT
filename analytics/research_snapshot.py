import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

rpct = pd.read_csv("data/rpct_scores.csv").iloc[-1]
forecast = pd.read_csv("data/forecast_signal.csv").iloc[-1]
shortage = pd.read_csv("data/shortage_probability.csv").iloc[-1]
providers = pd.read_csv("data/provider_rankings.csv")

md = f"""# AI-RPCT Research Snapshot

Generated: {datetime.now()}

## Current Infrastructure Risk

- RPCT Score: {rpct['score']}
- Regime: {rpct['regime']}
- Drivers: {rpct['drivers']}

## Forecast

- Forecast Score: {forecast['forecast_score']:.2f}
- Outlook: {forecast['outlook']}
- Shortage Probability: {shortage['shortage_probability']:.0f}%

## Provider Leaderboard

"""

for _, row in providers.iterrows():
    md += f"- {row['provider']}: score {row['score']:.2f}, price ${row['price_per_hour']:.2f}/hr, availability {row['availability']:.0f}\n"

filename = f"reports/research_snapshot_{datetime.now().strftime('%Y%m%d')}.md"

with open(filename, "w") as f:
    f.write(md)

print(md)
print(f"Saved: {filename}")
