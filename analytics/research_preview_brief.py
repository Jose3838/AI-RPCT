from datetime import datetime
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def build_research_preview_brief():
    readiness = read_latest(DATA_DIR / "core_intelligence_readiness.csv")
    paid_beta_gate = read_latest(DATA_DIR / "paid_beta_gate.csv")
    coverage = read_latest(DATA_DIR / "coverage_universe_status.csv")
    snapshot_quality = read_latest(DATA_DIR / "manual_snapshot_quality.csv")
    provenance = read_latest(DATA_DIR / "core_provenance_audit.csv")

    paid_allowed = str(paid_beta_gate.get("paid_beta_allowed", "False")).lower() == "true"
    snapshot_status = snapshot_quality.get("status", "unknown")
    coverage_status = coverage.get("status", "unknown")

    if paid_allowed:
        headline = "AI-RPCT is ready for controlled paid beta."
        preview_status = "paid_beta_ready"
    elif coverage_status == "universe_ready_snapshot_collection_needed":
        headline = "AI-RPCT research preview universe is ready; source-labeled snapshots are needed."
        preview_status = "snapshot_collection_needed"
    else:
        headline = "AI-RPCT remains in research preview while trust gates are cleared."
        preview_status = "research_preview"

    can_claim = [
        "Market universe tracks priority GPUs, providers and regions.",
        "Core intelligence methodology is implemented for scarcity, shock forecast and reliability.",
        "Manual public snapshots can be imported only with source labels and research-preview scope.",
        "Paid beta remains blocked until live data, provenance, history and commercial gates are green.",
    ]
    cannot_claim = [
        "No paid live-data reliability claim while provider ingestion uses fallback data.",
        "No 6-12 month history claim without sourced historical records.",
        "No region-level market coverage claim until valid source-labeled snapshots exist.",
    ]

    markdown = [
        "# AI-RPCT Research Preview Brief",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        f"## Headline",
        headline,
        "",
        "## Current Status",
        f"- Preview Status: {preview_status}",
        f"- Core Readiness Phase: {readiness.get('readiness_phase', 'n/a')}",
        f"- Paid Beta Gate: {paid_beta_gate.get('gate_status', 'n/a')} (allowed: {paid_beta_gate.get('paid_beta_allowed', False)})",
        f"- Coverage Status: {coverage_status}",
        f"- Manual Snapshot Quality: {snapshot_status}",
        f"- Valid Manual Snapshots: {snapshot_quality.get('valid_snapshot_count', 0)}",
        f"- GPU Universe: {coverage.get('gpu_universe_count', 'n/a')}",
        f"- Provider Universe: {coverage.get('provider_universe_count', 'n/a')}",
        f"- Region Universe: {coverage.get('region_universe_count', 'n/a')}",
        f"- Provenance: {provenance.get('provenance_band', 'n/a')}",
        "",
        "## Safe Claims",
        *[f"- {item}" for item in can_claim],
        "",
        "## Claims Not Yet Safe",
        *[f"- {item}" for item in cannot_claim],
        "",
        "## Next Action",
        snapshot_quality.get(
            "next_action",
            coverage.get("next_action", "Continue daily research-preview collection."),
        ),
    ]

    return {
        "product": "AI-RPCT",
        "report_type": "research_preview_brief",
        "generated_at": datetime.now().isoformat(),
        "preview_status": preview_status,
        "headline": headline,
        "core_readiness_phase": readiness.get("readiness_phase"),
        "paid_beta_gate_status": paid_beta_gate.get("gate_status"),
        "paid_beta_allowed": paid_allowed,
        "coverage_status": coverage_status,
        "manual_snapshot_quality_status": snapshot_status,
        "valid_manual_snapshot_count": snapshot_quality.get("valid_snapshot_count", 0),
        "gpu_universe_count": coverage.get("gpu_universe_count"),
        "provider_universe_count": coverage.get("provider_universe_count"),
        "region_universe_count": coverage.get("region_universe_count"),
        "provenance_band": provenance.get("provenance_band"),
        "safe_claims": can_claim,
        "unsafe_claims": cannot_claim,
        "next_action": snapshot_quality.get(
            "next_action",
            coverage.get("next_action", "Continue daily research-preview collection."),
        ),
        "markdown": "\n".join(markdown),
    }


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    brief = build_research_preview_brief()
    stamp = datetime.now().strftime("%Y%m%d")
    path = REPORTS_DIR / f"research_preview_brief_{stamp}.md"
    path.write_text(brief["markdown"])
    print(pd.DataFrame([{key: value for key, value in brief.items() if key != "markdown"}]))


if __name__ == "__main__":
    main()
