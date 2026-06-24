import pandas as pd

moat = pd.read_csv("data/evidence_moat_score.csv")
coverage = pd.read_csv("data/coverage_universe_status.csv")

m = moat.iloc[-1]
c = coverage.iloc[-1]

score = round(
    (
        float(m["score"]) * 0.5 +
        float(c["gpu_coverage_pct"]) * 0.2 +
        float(c["provider_coverage_pct"]) * 0.15 +
        float(c["region_coverage_pct"]) * 0.15
    ),
    2
)

if score >= 80:
    status = "investor_grade"
elif score >= 60:
    status = "commercial_grade"
else:
    status = "research_grade"

row = {
    "product": "AI-RPCT",
    "report_type": "evidence_intelligence_score",
    "score": score,
    "status": status
}

pd.DataFrame([row]).to_csv(
    "data/evidence_intelligence_score.csv",
    index=False
)

print(pd.DataFrame([row]))
