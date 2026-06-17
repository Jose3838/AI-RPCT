import pandas as pd
from pathlib import Path

checks = {
    "public_api": True,
    "web_terminal": Path("web/index.html").exists(),
    "live_provider_data": Path("data/live_provider_data.csv").exists() and Path("data/runpod_live_report.csv").exists(),
    "weekly_report": any(Path("reports").glob("weekly_infrastructure_report_*.txt")),
    "investor_snapshot": any(Path("reports").glob("investor_snapshot_*.txt")),
    "terms_draft": Path("docs/TERMS_DRAFT.md").exists(),
    "trust_center": Path("docs/TRUST_CENTER.md").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "sales_readiness_score": score,
    "recommended_action": "start_customer_discovery" if score >= 80 else "keep_building",
    **checks
}])

out.to_csv("data/sales_readiness.csv", index=False)

print(out)
