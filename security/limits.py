from datetime import datetime
from pathlib import Path

import pandas as pd


LIMITS_FILE = Path("data/plan_limits.csv")


def read_plan_limits():
    if not LIMITS_FILE.exists() or LIMITS_FILE.stat().st_size <= 1:
        return {}

    records = pd.read_csv(LIMITS_FILE).to_dict(orient="records")
    limits = {}

    for row in records:
        plan = row.get("plan")
        if not plan:
            continue

        limits[str(plan)] = {
            "requests_per_day": int(row.get("requests_per_day", 0)),
            "requests_per_month": int(row.get("requests_per_month", 0)),
            "features": str(row.get("features", "")),
        }

    return limits


def parse_usage_timestamp(value):
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return None


def count_usage(records, now=None):
    now = now or datetime.now()
    today = now.date()
    month = (now.year, now.month)
    daily_calls = 0
    monthly_calls = 0

    for row in records:
        timestamp = parse_usage_timestamp(row.get("timestamp"))
        if timestamp is None:
            continue

        if timestamp.date() == today:
            daily_calls += 1

        if (timestamp.year, timestamp.month) == month:
            monthly_calls += 1

    return {
        "daily_calls": daily_calls,
        "monthly_calls": monthly_calls,
    }


def build_limit_status(plan, usage_records, now=None):
    limits = read_plan_limits().get(plan)
    usage = count_usage(usage_records, now)

    if not limits:
        return {
            "plan": plan,
            "limited": True,
            "reason": "missing_plan_limits",
            "limits": {},
            **usage,
        }

    daily_limit = limits["requests_per_day"]
    monthly_limit = limits["requests_per_month"]
    daily_remaining = max(daily_limit - usage["daily_calls"], 0)
    monthly_remaining = max(monthly_limit - usage["monthly_calls"], 0)
    limited = daily_remaining <= 0 or monthly_remaining <= 0

    reason = None
    if daily_remaining <= 0:
        reason = "daily_limit_exceeded"
    elif monthly_remaining <= 0:
        reason = "monthly_limit_exceeded"

    return {
        "plan": plan,
        "limited": limited,
        "reason": reason,
        "limits": limits,
        **usage,
        "daily_remaining": daily_remaining,
        "monthly_remaining": monthly_remaining,
    }
