from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

changes = read_csv(DATA_DIR / "manual_snapshot_changes.csv")
moat = read_csv(DATA_DIR / "evidence_moat_score_v2.csv")
coverage = read_csv(DATA_DIR / "coverage_universe_status.csv")
priority = read_csv(DATA_DIR / "coverage_gap_priority.csv")

moat_row = moat.iloc[-1].to_dict() if not moat.empty else {}
coverage_row = coverage.iloc[-1].to_dict() if not coverage.empty else {}

top_gaps = priority.head(5).to_dict(orient="records") if not priority.empty else []
change_count = len(changes)

if change_count > 0:
    headline = f"{change_count} market evidence changes detected."
else:
    headline = "No material evidence changes detected."

summary = (
    f"Evidence moat status is {moat_row.get('status', 'unknown')} "
    f"with score {moat_row.get('score', 'n/a')}. "
    f"GPU coverage is {coverage_row.get('gpu_coverage_pct', 'n/a')}%, "
    f"provider coverage is {coverage_row.get('provider_coverage_pct', 'n/a')}%, "
    f"region coverage is {coverage_row.get('region_coverage_pct', 'n/a')}%."
)

row = {
    "product": "AI-RPCT",
    "report_type": "customer_intelligence_feed",
    "headline": headline,
    "summary": summary,
    "change_count": change_count,
    "evidence_moat_score": moat_row.get("score", ""),
    "evidence_moat_status": moat_row.get("status", ""),
    "gpu_coverage_pct": coverage_row.get("gpu_coverage_pct", ""),
    "provider_coverage_pct": coverage_row.get("provider_coverage_pct", ""),
    "region_coverage_pct": coverage_row.get("region_coverage_pct", ""),
    "top_gap_count": len(top_gaps),
    "claim_scope": "research_preview",
    "recommended_action": "Review top coverage gaps and maintain daily source-backed evidence collection."
}

pd.DataFrame([row]).to_csv(DATA_DIR / "customer_intelligence_feed.csv", index=False)

with open(REPORTS_DIR / "customer_intelligence_feed.md", "w") as f:
    f.write("# AI-RPCT Customer Intelligence Feed\n\n")
    f.write(f"## Headline\n{headline}\n\n")
    f.write(f"## Summary\n{summary}\n\n")
    f.write("## Top Coverage Gaps\n")
    for gap in top_gaps:
        f.write(f"- {gap.get('gap_type')}: {gap.get('target')} | impact {gap.get('impact_score')}\n")

print(pd.DataFrame([row]))
