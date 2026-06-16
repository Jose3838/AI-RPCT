import pandas as pd
from datetime import date

brief = f"""
AI-RPCT Investor Brief
Date: {date.today()}

Key Metrics:
- Providers tracked: {len(pd.read_csv('data/provider_rankings.csv'))}
- Active alerts: {len(pd.read_csv('data/alerts.csv'))}
- Data quality score:
  {pd.read_csv('data/data_quality.csv')['data_quality_score'].iloc[0]}%
"""

with open(
    "reports/investor_brief.txt",
    "w"
) as f:
    f.write(brief)

print(brief)
