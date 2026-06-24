import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.coverage_universe_status import build_coverage_universe_status
from analytics.manual_snapshot_ingest import ensure_columns
from analytics.manual_snapshot_quality import (
    build_manual_snapshot_quality,
    filter_valid_manual_snapshots,
    read_csv,
)
from analytics.snapshot_collection_plan import build_snapshot_collection_plan
from scripts.manual_snapshot_template_check import build_manual_snapshot_template_check


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


def read_snapshot_frame(path):
    frame = read_csv(path)
    return ensure_columns(frame) if not frame.empty else frame


def build_next_actions(collection_plan, limit=20):
    actions = []
    for index, row in collection_plan.head(limit).reset_index(drop=True).iterrows():
        actions.append({
            "rank": int(index + 1),
            "action_type": "collect_source_labeled_snapshot",
            "provider": row.get("provider"),
            "gpu": row.get("gpu"),
            "region_code": row.get("region_code"),
            "priority_score": row.get("priority_score"),
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "operator_step": (
                "Find a public source page, fill price_per_hour, availability, "
                "delivery_time_days and source_url in data/manual_market_snapshot_inbox_template.csv."
            ),
        })
    return actions


def build_manual_snapshot_daily_pack(data_dir=DATA_DIR, action_limit=20):
    data_dir = Path(data_dir)
    template = read_snapshot_frame(data_dir / "manual_market_snapshot_inbox_template.csv")
    inbox = read_snapshot_frame(data_dir / "manual_market_snapshot_inbox.csv")
    master = read_snapshot_frame(data_dir / "manual_market_snapshots.csv")
    rejections = read_csv(data_dir / "manual_market_snapshot_rejections.csv")
    template_rejections = read_csv(data_dir / "manual_market_snapshot_template_rejections.csv")
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")

    valid_master = filter_valid_manual_snapshots(
        master,
        gpu_universe,
        provider_universe,
        region_universe,
    )
    quality = build_manual_snapshot_quality(data_dir).iloc[0].to_dict()
    coverage = build_coverage_universe_status(data_dir).iloc[0].to_dict()
    template_check = build_manual_snapshot_template_check(data_dir)
    collection_plan = build_snapshot_collection_plan(data_dir, limit=action_limit)
    next_actions = build_next_actions(collection_plan, limit=action_limit)

    if template_check["valid_row_count"] > 0:
        next_action = "Copy ready template rows, then ingest manual snapshots."
    elif len(inbox) > 0:
        next_action = "Run manual snapshot ingest and review rejected inbox rows."
    elif int(quality.get("valid_snapshot_count", 0)) == 0:
        next_action = "Fill the top source-labeled snapshot targets before tomorrow's run."
    else:
        next_action = "Continue collecting source-labeled snapshots from the next action list."

    summary = {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_daily_pack",
        "status": quality.get("status", "unknown"),
        "coverage_status": coverage.get("status", "unknown"),
        "template_status": template_check.get("status", "unknown"),
        "template_row_count": int(len(template)),
        "template_valid_row_count": int(template_check.get("valid_row_count", 0)),
        "inbox_row_count": int(len(inbox)),
        "master_snapshot_count": int(len(master)),
        "valid_master_snapshot_count": int(len(valid_master)),
        "rejected_inbox_row_count": int(len(rejections)),
        "rejected_template_row_count": int(len(template_rejections)),
        "gpu_coverage_pct": coverage.get("gpu_coverage_pct", 0.0),
        "provider_coverage_pct": coverage.get("provider_coverage_pct", 0.0),
        "region_coverage_pct": coverage.get("region_coverage_pct", 0.0),
        "claim_scope": "research_preview",
        "history_policy": "do_not_backfill_without_sources",
        "blockers": quality.get("blockers", "unknown"),
        "coverage_blockers": coverage.get("blockers", "unknown"),
        "next_action_count": len(next_actions),
        "next_action": next_action,
    }

    return {
        "summary": summary,
        "next_actions": next_actions,
        "template_check": template_check,
    }


def save_manual_snapshot_daily_pack(data_dir=DATA_DIR, reports_dir=REPORTS_DIR):
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)
    pack = build_manual_snapshot_daily_pack(data_dir)
    pd.DataFrame([pack["summary"]]).to_csv(
        data_dir / "manual_snapshot_daily_pack.csv",
        index=False,
    )
    pd.DataFrame(pack["next_actions"]).to_csv(
        data_dir / "manual_snapshot_next_20_actions.csv",
        index=False,
    )
    (data_dir / "manual_snapshot_daily_pack.json").write_text(json.dumps(pack, indent=2))
    save_manual_snapshot_markdown(pack, reports_dir=reports_dir)
    return pack


def save_manual_snapshot_markdown(pack, reports_dir=REPORTS_DIR):
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(exist_ok=True)
    summary = pack["summary"]
    lines = [
        "# AI-RPCT Manual Snapshot Next 20",
        "",
        f"Status: {summary.get('status')}",
        f"Coverage: {summary.get('coverage_status')}",
        f"Template: {summary.get('template_status')}",
        f"Valid manual snapshots: {summary.get('valid_master_snapshot_count')}",
        f"Coverage pct: GPU {summary.get('gpu_coverage_pct')}%, provider {summary.get('provider_coverage_pct')}%, region {summary.get('region_coverage_pct')}%",
        f"Claim scope: {summary.get('claim_scope')}",
        f"Policy: {summary.get('history_policy')}",
        "",
        f"Next action: {summary.get('next_action')}",
        "",
        "## Next 20 Actions",
        "",
    ]
    for action in pack["next_actions"]:
        lines.append(
            f"{action['rank']}. {action['provider']} / {action['gpu']} / {action['region_code']} "
            f"- collect source URL, price, availability, delivery time."
        )
    lines.append("")
    lines.append("Do not backfill without source evidence.")

    path = reports_dir / "manual_snapshot_next_20_actions.md"
    path.write_text("\n".join(lines))
    return {
        "status": "saved",
        "file": str(path),
        "action_count": len(pack["next_actions"]),
    }


def main():
    print(json.dumps(save_manual_snapshot_daily_pack(), indent=2))


if __name__ == "__main__":
    main()
