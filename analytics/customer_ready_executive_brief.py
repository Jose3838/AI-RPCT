from datetime import datetime
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
SUMMARY_FILE = DATA_DIR / "customer_ready_executive_brief_summary.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_records(path, limit=5):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).head(limit).to_dict(orient="records")


def safe_value(row, key, fallback="n/a"):
    value = row.get(key, fallback)
    if pd.isna(value):
        return fallback
    return value


def build_customer_ready_executive_brief():
    generated_at = datetime.now().isoformat()
    morning = read_latest(DATA_DIR / "morning_brief_summary.csv")
    performance = read_latest(DATA_DIR / "signal_performance_score.csv")
    claim_gate = read_records(DATA_DIR / "claim_gate_matrix.csv", limit=10)
    watchlist = read_records(DATA_DIR / "customer_watchlists.csv", limit=10)
    explainability = read_records(DATA_DIR / "signal_explainability_drilldowns.csv", limit=8)
    evidence = read_records(DATA_DIR / "source_evidence_view.csv", limit=8)

    allowed_claims = [
        row for row in claim_gate
        if str(row.get("allowed", "")).lower() == "true"
    ]
    blocked_claims = [
        row for row in claim_gate
        if str(row.get("allowed", "")).lower() != "true"
    ]

    headline = (
        f"AI infrastructure stress is {safe_value(morning, 'stress_band')}; "
        f"signal performance is {safe_value(performance, 'performance_band')}."
    )
    customer_decision = safe_value(morning, "today_action", "Maintain daily monitoring.")
    claim_posture = "research_preview"
    if not blocked_claims and allowed_claims:
        claim_posture = "paid_safe_candidate"

    watch_lines = [
        f"- {row.get('watch_type')}: {row.get('name')} ({row.get('priority')}) -> {row.get('next_action')}"
        for row in watchlist
    ] or ["- No watchlist rows available."]
    explain_lines = [
        f"- {row.get('signal')} / {row.get('component')}: {row.get('value')} ({row.get('weight')})"
        for row in explainability
    ] or ["- No explainability rows available."]
    evidence_lines = [
        f"- {row.get('provider', 'n/a')} / {row.get('gpu', 'n/a')} / {row.get('region_code', 'n/a')}: {row.get('evidence_quality', 'n/a')}"
        for row in evidence
    ] or ["- No source evidence rows available."]

    markdown = "\n".join([
        "# AI-RPCT Customer-Ready Executive Brief",
        "",
        f"Generated: {generated_at}",
        "",
        "## Headline",
        headline,
        "",
        "## Decision",
        customer_decision,
        "",
        "## Signal Performance",
        f"- Score: {safe_value(performance, 'signal_performance_score', 0)}",
        f"- Band: {safe_value(performance, 'performance_band')}",
        f"- Blockers: {safe_value(performance, 'blockers')}",
        "",
        "## Claim Posture",
        f"- Current posture: {claim_posture}",
        f"- Allowed claim gates: {len(allowed_claims)}",
        f"- Blocked claim gates: {len(blocked_claims)}",
        "",
        "## Customer Watchlist",
        *watch_lines,
        "",
        "## Explainability Drilldown",
        *explain_lines,
        "",
        "## Source Evidence",
        *evidence_lines,
        "",
        "## Guardrail",
        "This brief is research-preview unless all claim gates are paid-safe.",
    ])

    return {
        "product": "AI-RPCT",
        "report_type": "customer_ready_executive_brief",
        "generated_at": generated_at,
        "headline": headline,
        "customer_decision": customer_decision,
        "claim_posture": claim_posture,
        "signal_performance_score": safe_value(performance, "signal_performance_score", 0),
        "performance_band": safe_value(performance, "performance_band"),
        "allowed_claim_gate_count": len(allowed_claims),
        "blocked_claim_gate_count": len(blocked_claims),
        "watchlist_count": len(watchlist),
        "source_evidence_count": len(evidence),
        "markdown": markdown,
    }


def main():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    brief = build_customer_ready_executive_brief()
    report_file = REPORTS_DIR / f"customer_ready_executive_brief_{datetime.now().strftime('%Y%m%d')}.md"
    report_file.write_text(brief["markdown"])
    summary = pd.DataFrame([{key: value for key, value in brief.items() if key != "markdown"}])
    summary.to_csv(SUMMARY_FILE, index=False)
    print(summary)


if __name__ == "__main__":
    main()
