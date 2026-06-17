from pathlib import Path
import pandas as pd

checks = {
    "usage_plans": Path("data/usage_plan_matrix.csv").exists(),
    "plan_access_matrix": Path("data/plan_access_matrix.csv").exists(),
    "api_key_registry": Path("data/api_key_registry.csv").exists(),
    "plan_resolver": Path("security/plan_resolver.py").exists(),
    "entitlement_checker": Path("security/entitlements.py").exists(),
    "pricing_doc": Path("docs/PRICING.md").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "monetization_readiness_score": score,
    **checks
}])

out.to_csv("data/monetization_readiness.csv", index=False)

print(out)
