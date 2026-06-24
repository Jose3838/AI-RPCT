from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

moat = read_csv(DATA_DIR / "evidence_moat_score.csv")
coverage = read_csv(DATA_DIR / "coverage_universe_status.csv")
quality = read_csv(DATA_DIR / "manual_snapshot_quality.csv")
source = read_csv(DATA_DIR / "source_url_coverage_metrics.csv")
history = read_csv(DATA_DIR / "manual_snapshot_history_audit.csv")
changes = read_csv(DATA_DIR / "manual_snapshot_changes.csv")
priority = read_csv(DATA_DIR / "coverage_gap_priority.csv")

m = moat.iloc[-1].to_dict() if not moat.empty else {}
c = coverage.iloc[-1].to_dict() if not coverage.empty else {}
q = quality.iloc[-1].to_dict() if not quality.empty else {}
s = source.iloc[-1].to_dict() if not source.empty else {}

base_score = float(m.get("score", 0))
source_score = float(s.get("source_url_coverage_pct", 0))
coverage_blend = (
    float(c.get("gpu_coverage_pct", 0)) * 0.4 +
    float(c.get("provider_coverage_pct", 0)) * 0.3 +
    float(c.get("region_coverage_pct", 0)) * 0.3
)

history_depth_score = min(100, len(history) * 10)
change_intelligence_score = min(100, len(changes) * 5)
gap_priority_penalty = min(25, len(priority) * 1.2)

score = round(
    base_score * 0.30 +
    source_score * 0.15 +
    coverage_blend * 0.25 +
    history_depth_score * 0.15 +
    change_intelligence_score * 0.15 -
    gap_priority_penalty,
    2
)

if score >= 80:
    status = "institutional_evidence_moat"
elif score >= 60:
    status = "commercial_evidence_moat"
elif score >= 40:
    status = "building_evidence_moat"
else:
    status = "thin_evidence_moat"

row = {
    "product": "AI-RPCT",
    "report_type": "evidence_moat_score_v2",
    "score": max(0, score),
    "status": status,
    "base_evidence_moat_score": base_score,
    "source_url_coverage_pct": source_score,
    "coverage_blend": round(coverage_blend, 2),
    "history_depth_score": history_depth_score,
    "change_intelligence_score": change_intelligence_score,
    "open_gap_count": len(priority),
    "gap_priority_penalty": gap_priority_penalty,
    "claim_scope": "research_preview",
    "next_action": "Close highest-impact coverage gaps and collect daily comparable snapshots."
}

pd.DataFrame([row]).to_csv(DATA_DIR / "evidence_moat_score_v2.csv", index=False)
print(pd.DataFrame([row]))
