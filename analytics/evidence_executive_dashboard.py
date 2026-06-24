import pandas as pd

moat = pd.read_csv("data/evidence_moat_score.csv")
intel = pd.read_csv("data/evidence_intelligence_score.csv")
coverage = pd.read_csv("data/coverage_universe_status.csv")

row = {
    "evidence_moat_score": moat.iloc[-1]["score"],
    "evidence_intelligence_score": intel.iloc[-1]["score"],
    "gpu_coverage_pct": coverage.iloc[-1]["gpu_coverage_pct"],
    "provider_coverage_pct": coverage.iloc[-1]["provider_coverage_pct"],
    "region_coverage_pct": coverage.iloc[-1]["region_coverage_pct"]
}

pd.DataFrame([row]).to_csv(
    "data/evidence_executive_dashboard.csv",
    index=False
)

print(pd.DataFrame([row]))
