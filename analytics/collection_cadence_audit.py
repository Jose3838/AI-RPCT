from datetime import date
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "collection_cadence_audit.csv"
MILESTONES = [30, 90, 180, 365]


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def parse_dates(values):
    parsed = []
    for value in values:
        try:
            parsed.append(pd.to_datetime(value).date())
        except (TypeError, ValueError):
            continue
    return sorted(set(parsed))


def consecutive_streak(dates):
    if not dates:
        return 0
    streak = 1
    current = dates[-1]
    for previous in reversed(dates[:-1]):
        if (current - previous).days == 1:
            streak += 1
            current = previous
            continue
        break
    return streak


def missing_dates_between(dates):
    if len(dates) < 2:
        return []
    expected = pd.date_range(dates[0], dates[-1], freq="D").date
    collected = set(dates)
    return [day.isoformat() for day in expected if day not in collected]


def next_milestone(days_collected):
    for milestone in MILESTONES:
        if days_collected < milestone:
            return milestone
    return MILESTONES[-1]


def build_collection_cadence_audit(data_dir=DATA_DIR, today=None):
    data_dir = Path(data_dir)
    today = today or date.today()
    history = read_csv(data_dir / "core_signal_history.csv")
    dates = parse_dates(history.get("date", [])) if not history.empty else []
    days_collected = len(dates)
    missing = missing_dates_between(dates)
    latest_date = dates[-1] if dates else None
    latest_age_days = (today - latest_date).days if latest_date else None
    streak = consecutive_streak(dates)
    milestone = next_milestone(days_collected)
    days_to_milestone = max(0, milestone - days_collected)

    if days_collected == 0:
        status = "no_history"
        next_action = "Run ./scripts/run_core_intelligence.sh daily to start the intelligence time series."
    elif latest_age_days is not None and latest_age_days > 1:
        status = "stale_collection"
        next_action = "Wake the Mac or run ./scripts/run_core_intelligence.sh to restore daily collection."
    elif missing:
        status = "history_has_gaps"
        next_action = "Keep daily collection running; do not backfill missing days without source evidence."
    elif days_collected >= 30:
        status = "paid_beta_cadence_ready"
        next_action = "Maintain daily collection and improve source quality."
    else:
        status = "building_history"
        next_action = f"Collect {days_to_milestone} more daily records to reach the {milestone}-day milestone."

    return pd.DataFrame([{
        "status": status,
        "days_collected": int(days_collected),
        "current_streak_days": int(streak),
        "latest_date": latest_date.isoformat() if latest_date else "",
        "latest_age_days": latest_age_days if latest_age_days is not None else "",
        "missing_day_count": int(len(missing)),
        "missing_dates": "|".join(missing[:20]),
        "next_milestone_days": int(milestone),
        "days_to_next_milestone": int(days_to_milestone),
        "history_policy": "do_not_backfill_without_sources",
        "next_action": next_action,
    }])


def main():
    result = build_collection_cadence_audit()
    DATA_DIR.mkdir(exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
