import pandas as pd
from pathlib import Path

checks = {
    "api_catalog": Path("data/api_catalog.csv").exists(),
    "public_roadmap": Path("docs/PUBLIC_ROADMAP.md").exists(),
    "pricing": Path("docs/PRICING.md").exists(),
    "beta_offer": Path("docs/BETA_OFFER.md").exists(),
    "web_terminal": Path("web/index.html").exists(),
    "live_provider_data": Path("data/live_provider_data.csv").exists() and Path("data/runpod_live_report.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "api_product_status_score": score,
    **checks
}])

out.to_csv("data/api_product_status.csv", index=False)

print(out)
