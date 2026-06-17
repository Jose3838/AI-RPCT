import pandas as pd
from pathlib import Path

checks = {
    "provider_rankings": Path("data/provider_rankings.csv").exists(),
    "provider_marketshare": Path("data/provider_marketshare.csv").exists(),
    "provider_concentration": Path("data/provider_concentration.csv").exists(),
    "provider_daily_metrics": Path("data/provider_daily_metrics.csv").exists(),
    "provider_dominance": Path("data/provider_dominance_index.csv").exists(),
    "real_provider_docs": Path("docs/REAL_PROVIDER_REQUIREMENTS.md").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "provider_intelligence_readiness": score,
    **checks
}])

out.to_csv("data/provider_intelligence_readiness.csv", index=False)

print(out)
