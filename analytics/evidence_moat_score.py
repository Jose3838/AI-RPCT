from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

coverage = read_csv(DATA_DIR / "coverage_universe_status.csv")
quality = read_csv(DATA_DIR / "manual_snapshot_quality.csv")
source = read_csv(DATA_DIR / "source_url_coverage_metrics.csv")
history = read_csv(DATA_DIR / "manual_snapshot_history_audit.csv")
gaps = read_csv(DATA_DIR / "coverage_gap_plan.csv")

c = coverage.iloc[-1].to_dict() if not coverage.empty else {}
q = quality.iloc[-1].to_dict() if not quality.empty else {}
s = source.iloc[-1].to_dict() if not source.empty else {}

snapshot_score = min(100, float(q.get("valid_snapshot_count", 0)) * 2)
source_score = float(s.get("source_url_coverage_pct", 0))
gpu_score = float(c.get("gpu_coverage_pct", 0))
provider_score = float(c.get("provider_coverage_pct", 0))
region_score = float(c.get("region_coverage_pct", 0))
history_score = min(100, len(history) * 20)
gap_penalty = min(30, len(gaps) * 1.5)

score = round(
    (
        snapshot_score * 0.20 +
        source_score * 0.20 +
        gpu_score * 0.20 +
        provider_score * 0.15 +
        region_score * 0.15 +
        history_score * 0.10
    ) - gap_penalty,
    2
)

if score >= 80:
    status = "strong_evidence_moat"
elif score >= 60:
    status = "building_evidence_moat"
else:
    status = "thin_evidence_moat"

row = {
    "product": "AI-RPCT",
    "report_type": "evidence_moat_score",
    "score": max(0, score),
    "status": status,
    "valid_snapshot_count": q.get("valid_snapshot_count", 0),
    "source_url_coverage_pct": source_score,
    "gpu_coverage_pct": gpu_score,
    "provider_coverage_pct": provider_score,
    "region_coverage_pct": region_score,
    "history_days": len(history),
    "open_gap_count": len(gaps),
    "claim_scope": "research_preview",
    "next_action": "Close priority GPU/provider/region gaps and keep daily source-backed history."
}

pd.DataFrame([row]).to_csv(DATA_DIR / "evidence_moat_score.csv", index=False)
print(pd.DataFrame([row]))
