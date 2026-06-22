from datetime import date, timedelta
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "core_signal_history.csv"
TARGET_DAYS = 30


def build_expected_dates(end_date=None, days=TARGET_DAYS):
    end_date = end_date or date.today()
    return [
        (end_date - timedelta(days=offset)).isoformat()
        for offset in range(days - 1, -1, -1)
    ]


def build_core_history_audit(history_file=HISTORY_FILE, end_date=None):
    history_file = Path(history_file)
    expected_dates = build_expected_dates(end_date=end_date)

    if not history_file.exists() or history_file.stat().st_size <= 1:
        observed_dates = set()
        latest_date = None
    else:
        history = pd.read_csv(history_file)
        observed_dates = set(history.get("date", pd.Series(dtype=str)).dropna().astype(str))
        latest_date = max(observed_dates) if observed_dates else None

    missing_dates = [day for day in expected_dates if day not in observed_dates]
    days_collected = len(observed_dates)
    progress_pct = round(min(100.0, (days_collected / TARGET_DAYS) * 100), 2)

    if days_collected >= TARGET_DAYS and not missing_dates:
        history_band = "paid_beta_ready"
    elif days_collected >= 14:
        history_band = "forming_moat"
    elif days_collected >= 7:
        history_band = "early_signal"
    elif days_collected > 0:
        history_band = "thin_history"
    else:
        history_band = "empty"

    stale_days = 0
    if latest_date:
        today = end_date or date.today()
        stale_days = (today - date.fromisoformat(latest_date)).days

    return pd.DataFrame([{
        "target_days": TARGET_DAYS,
        "days_collected": days_collected,
        "days_remaining": max(0, TARGET_DAYS - days_collected),
        "progress_pct": progress_pct,
        "history_band": history_band,
        "latest_date": latest_date or "",
        "stale_days": stale_days,
        "missing_recent_days": ", ".join(missing_dates[-7:]) if missing_dates else "none",
        "paid_beta_history_ready": days_collected >= TARGET_DAYS and not missing_dates,
    }])


def main():
    audit = build_core_history_audit()
    audit.to_csv(DATA_DIR / "core_history_audit.csv", index=False)
    print(audit)


if __name__ == "__main__":
    main()
