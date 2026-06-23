from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
OUTPUT_FILE = DATA_DIR / "bloomberg_execution_roadmap.csv"


ROADMAP = [
    # Data moat
    ("data_moat", 1, "Collect source-labeled public GPU price snapshots daily.", "in_progress", "data/manual_market_snapshots.csv"),
    ("data_moat", 2, "Expand priority coverage to 20+ GPU types.", "done", "data/gpu_universe.csv"),
    ("data_moat", 3, "Expand priority coverage to 15+ providers.", "done", "data/provider_universe.csv"),
    ("data_moat", 4, "Track priority regions for region-level pressure.", "done", "data/region_universe.csv"),
    ("data_moat", 5, "Reach 30 clean daily core signal records.", "in_progress", "data/core_signal_history.csv"),
    ("data_moat", 6, "Reach 90 clean daily core signal records.", "not_started", "data/core_signal_history.csv"),
    ("data_moat", 7, "Reach 180 clean daily core signal records.", "not_started", "data/core_signal_history.csv"),
    ("data_moat", 8, "Track manual snapshot quality and rejection reasons.", "done", "data/manual_snapshot_quality.csv"),
    ("data_moat", 9, "Track collection cadence and missing history days.", "done", "data/collection_cadence_audit.csv"),
    ("data_moat", 10, "Build source provenance for every paid-facing data point.", "in_progress", "data/core_provenance_audit.csv"),
    # Trust and methodology
    ("trust", 11, "Document each core signal methodology.", "done", "data/signal_methodology_registry.csv"),
    ("trust", 12, "Gate every claim as research-preview or paid-safe.", "in_progress", "data/paid_beta_gate.csv"),
    ("trust", 13, "Expose signal trust status in terminal summary.", "in_progress", "api/terminal_core.py"),
    ("trust", 14, "Separate fallback data from live provider data.", "done", "data/provider_preflight.csv"),
    ("trust", 15, "Create customer-facing trust center copy.", "done", "docs/TRUST_CENTER.md"),
    ("trust", 16, "Add forecast accuracy backtesting to paid-readiness gates.", "in_progress", "data/forecast_accuracy.csv"),
    ("trust", 17, "Add source URL coverage metrics by provider/GPU/region.", "not_started", "data/manual_market_snapshots.csv"),
    ("trust", 18, "Add confidence score for each morning brief recommendation.", "not_started", "analytics/morning_brief.py"),
    ("trust", 19, "Publish safe-claims and unsafe-claims in research preview.", "done", "reports/research_preview_brief_*.md"),
    ("trust", 20, "Create methodology changelog for signal formula changes.", "not_started", "docs"),
    # Core intelligence
    ("core_intelligence", 21, "Strengthen GPU Scarcity Index with source-backed observations.", "in_progress", "data/gpu_scarcity_index.csv"),
    ("core_intelligence", 22, "Strengthen Capacity Shock Forecast with validation history.", "in_progress", "data/forecast_signal.csv"),
    ("core_intelligence", 23, "Strengthen Provider Reliability Score with live ingestion.", "in_progress", "data/provider_reliability_ranking.csv"),
    ("core_intelligence", 24, "Add Price Dislocation Signal.", "not_started", "analytics"),
    ("core_intelligence", 25, "Add AI Infrastructure Stress Index composite.", "not_started", "analytics"),
    ("core_intelligence", 26, "Add region-level scarcity heatmap data.", "not_started", "data/manual_market_snapshots.csv"),
    ("core_intelligence", 27, "Add provider recovery and credential readiness plan.", "done", "scripts/provider_recovery_plan.py"),
    ("core_intelligence", 28, "Add collection target planner for manual snapshots.", "done", "data/snapshot_collection_plan.csv"),
    ("core_intelligence", 29, "Add daily provider reliability gap analysis.", "done", "data/provider_reliability_gaps.csv"),
    ("core_intelligence", 30, "Add signal performance score over time.", "in_progress", "data/core_signal_quality.csv"),
    # Terminal product
    ("terminal_product", 31, "Generate daily AI Infrastructure Morning Brief.", "done", "reports/morning_brief_*.md"),
    ("terminal_product", 32, "Expose structured morning brief in terminal summary.", "done", "data/morning_brief_summary.csv"),
    ("terminal_product", 33, "Create customer-ready executive brief.", "in_progress", "reports/executive_ai_infrastructure_memo_*.txt"),
    ("terminal_product", 34, "Add actionable alerts for scarcity, shock and reliability drops.", "not_started", "analytics"),
    ("terminal_product", 35, "Add latest reports registry for customer consumption.", "done", "api/terminal_core.py"),
    ("terminal_product", 36, "Add daily founder close for next-session continuity.", "done", "scripts/founder_daily_close.py"),
    ("terminal_product", 37, "Create terminal UI focused on morning decisions.", "in_progress", "web"),
    ("terminal_product", 38, "Add explain-this-score drilldowns.", "not_started", "web"),
    ("terminal_product", 39, "Add source evidence viewer for manual snapshots.", "not_started", "web"),
    ("terminal_product", 40, "Add customer watchlists for GPUs/providers/regions.", "not_started", "web"),
    # Commercial and distribution
    ("commercial", 41, "Define ICP and buying trigger.", "done", "docs/ICP.md"),
    ("commercial", 42, "Package research preview for first design partners.", "in_progress", "docs/BETA_OFFER.md"),
    ("commercial", 43, "Create weekly public AI infrastructure stress report.", "in_progress", "reports/weekly_infrastructure_report_*.txt"),
    ("commercial", 44, "Build customer report export.", "done", "intelligence/reports/customer_report_pdf_export_v1.py"),
    ("commercial", 45, "Create first paid-beta readiness checklist.", "done", "docs/BETA_CHECKLIST.md"),
    ("commercial", 46, "Add billing and entitlement hardening for paid beta.", "in_progress", "api/access.py"),
    ("commercial", 47, "Create outreach sequence and demo script.", "done", "docs/OUTREACH_SCRIPT.md"),
    ("commercial", 48, "Secure first design partner feedback loop.", "not_started", "docs/CUSTOMER_DISCOVERY.md"),
    ("commercial", 49, "Set first paid price and offer terms.", "in_progress", "docs/PRICING.md"),
    ("commercial", 50, "Ship public credibility page with methodology and sample brief.", "not_started", "docs"),
]


def build_bloomberg_execution_roadmap():
    rows = []
    for category, step, action, status, evidence in ROADMAP:
        rows.append({
            "category": category,
            "step": step,
            "action": action,
            "status": status,
            "evidence": evidence,
        })
    return pd.DataFrame(rows)


def build_roadmap_summary(roadmap=None):
    roadmap = roadmap if roadmap is not None else build_bloomberg_execution_roadmap()
    total = len(roadmap)
    done = int((roadmap["status"] == "done").sum())
    in_progress = int((roadmap["status"] == "in_progress").sum())
    not_started = int((roadmap["status"] == "not_started").sum())
    next_steps = roadmap[roadmap["status"] != "done"].head(10).to_dict(orient="records")
    return {
        "product": "AI-RPCT",
        "report_type": "bloomberg_execution_roadmap",
        "total_steps": total,
        "done_steps": done,
        "in_progress_steps": in_progress,
        "not_started_steps": not_started,
        "completion_pct": round((done / total) * 100, 2) if total else 0,
        "next_steps": next_steps,
    }


def build_roadmap_markdown(roadmap=None):
    roadmap = roadmap if roadmap is not None else build_bloomberg_execution_roadmap()
    summary = build_roadmap_summary(roadmap)
    lines = [
        "# AI-RPCT Bloomberg Execution Roadmap",
        "",
        f"Total Steps: {summary['total_steps']}",
        f"Done: {summary['done_steps']}",
        f"In Progress: {summary['in_progress_steps']}",
        f"Not Started: {summary['not_started_steps']}",
        f"Completion: {summary['completion_pct']}%",
        "",
    ]
    for category, group in roadmap.groupby("category", sort=False):
        lines.extend([f"## {category}", ""])
        for _, row in group.iterrows():
            lines.append(f"- [{row['status']}] {int(row['step'])}. {row['action']} ({row['evidence']})")
        lines.append("")
    return "\n".join(lines)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    roadmap = build_bloomberg_execution_roadmap()
    roadmap.to_csv(OUTPUT_FILE, index=False)
    (REPORTS_DIR / "bloomberg_execution_roadmap.md").write_text(build_roadmap_markdown(roadmap))
    print(pd.DataFrame([build_roadmap_summary(roadmap)]).drop(columns=["next_steps"]))


if __name__ == "__main__":
    main()
