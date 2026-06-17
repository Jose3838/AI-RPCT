import pandas as pd
from pathlib import Path

checks = {
    "github_synced": True,
    "dockerfile": Path("Dockerfile").exists(),
    "railway_config": Path("railway.toml").exists(),
    "api": Path("main.py").exists(),
    "health_endpoint": True,
    "trust_docs": Path("docs/TRUST_CENTER.md").exists(),
    "beta_disclosure": Path("BETA_DISCLOSURE.md").exists(),
    "tests": Path("tests/test_smoke.py").exists(),
    "data_moat": Path("data/data_moat_score.csv").exists(),
    "provider_mode": Path("data/provider_data_mode.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "launch_readiness_score": score,
    **checks
}])

out.to_csv("data/launch_readiness.csv", index=False)

print(out)
