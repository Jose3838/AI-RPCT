import pandas as pd
from pathlib import Path

checks = {
    "api": Path("main.py").exists(),
    "docker": Path("Dockerfile").exists(),
    "compose": Path("docker-compose.yml").exists(),
    "tests": Path("tests/test_smoke.py").exists(),
    "docs": Path("docs/PRODUCTION_CHECKLIST.md").exists(),
    "env_template": Path(".env.example").exists(),
    "real_provider_docs": Path("docs/REAL_PROVIDER_REQUIREMENTS.md").exists()
}

score = round(
    sum(checks.values()) / len(checks) * 100,
    2
)

pd.DataFrame([{
    "production_readiness_score": score,
    **checks
}]).to_csv(
    "data/production_readiness.csv",
    index=False
)

print("Production readiness:", score)
