import pandas as pd
from pathlib import Path

checks = {
    "dashboard": Path("web/index.html").exists(),
    "api_catalog": Path("data/api_catalog.csv").exists(),
    "usage_plans": Path("data/usage_plan_matrix.csv").exists(),
    "roadmap": Path("docs/PUBLIC_ROADMAP.md").exists(),
    "value_proposition": Path("docs/VALUE_PROPOSITION.md").exists(),
    "live_data_quality": Path("data/live_data_quality_score.csv").exists(),
    "provider_market_share": Path("data/live_provider_market_share.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "product_terminal_readiness_score": score,
    **checks
}])

out.to_csv("data/product_terminal_readiness.csv", index=False)

print(out)
