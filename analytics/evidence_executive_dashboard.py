import pandas as pd

moat = pd.read_csv("data/evidence_moat_score.csv")
coverage = pd.read_csv("data/coverage_universe_status.csv")
trend = pd.read_csv("data/evidence_trend_score.csv")

row = {
    "evidence_moat_score": moat.iloc[-1]["score"],
    "gpu_coverage_pct": coverage.iloc[-1]["gpu_coverage_pct"],
    "provider_coverage_pct": coverage.iloc[-1]["provider_coverage_pct"],
    "region_coverage_pct": coverage.iloc[-1]["region_coverage_pct"],
    "history_days": len(trend),
    "latest_snapshot_count": trend.iloc[-1]["snapshot_count"]
}

pd.DataFrame([row]).to_csv(
    "data/evidence_executive_dashboard.csv",
    index=False
)

print(pd.DataFrame([row]))
