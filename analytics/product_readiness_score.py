import pandas as pd
from pathlib import Path

checks = {
    "public_deployment": True,
    "web_terminal": Path("web/index.html").exists(),
    "live_vast": Path("data/live_provider_data.csv").exists(),
    "live_runpod": Path("data/runpod_live_report.csv").exists(),
    "reports": any(Path("reports").glob("*")) if Path("reports").exists() else False,
    "pricing": Path("docs/PRICING.md").exists(),
    "beta_offer": Path("docs/BETA_OFFER.md").exists(),
    "customer_pipeline": Path("data/customer_pipeline.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "product_readiness_score": score,
    **checks
}])

out.to_csv("data/product_readiness_score.csv", index=False)

print(out)
