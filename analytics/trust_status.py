import pandas as pd
from pathlib import Path

checks = {
    "terms_draft": Path("docs/TERMS_DRAFT.md").exists(),
    "privacy_draft": Path("docs/PRIVACY_DRAFT.md").exists(),
    "trust_center": Path("docs/TRUST_CENTER.md").exists(),
    "data_sources_api": Path("data/data_source_status.csv").exists(),
    "public_beta_status": Path("data/public_beta_status.csv").exists(),
    "commercial_readiness": Path("data/commercial_readiness.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "trust_readiness_score": score,
    **checks
}])

out.to_csv("data/trust_status.csv", index=False)

print(out)
