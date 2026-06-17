import pandas as pd
from pathlib import Path

checks = {
    "github_ready": True,
    "api_ready": Path("main.py").exists(),
    "docker_ready": Path("Dockerfile").exists(),
    "auth_foundation": Path("security/api_keys.py").exists(),
    "data_moat_started": Path("data/index_history.csv").exists(),
    "provider_mode_known": Path("data/provider_data_mode.csv").exists(),
    "live_provider_connected": False,
    "billing_ready": False,
    "terms_ready": False
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "commercial_readiness_score": score,
    **checks
}])

out.to_csv("data/commercial_readiness.csv", index=False)

print(out)
