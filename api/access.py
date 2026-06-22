from pathlib import Path

import pandas as pd
from fastapi import Header, HTTPException

from security.entitlements import has_access
from security.limits import build_limit_status, read_plan_limits
from security.plan_resolver import resolve_plan
from security.usage import USAGE_FILE, log_usage


ACCESS_FILE = Path("data/plan_access_matrix.csv")


def read_access_matrix():
    if not ACCESS_FILE.exists() or ACCESS_FILE.stat().st_size <= 1:
        return []
    return pd.read_csv(ACCESS_FILE).to_dict(orient="records")


def read_usage_records():
    path = Path(USAGE_FILE)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    records = pd.read_csv(path, on_bad_lines="skip").to_dict(orient="records")
    return [
        row for row in records
        if pd.notna(row.get("api_key")) and pd.notna(row.get("endpoint"))
    ]


def build_access_status(x_api_key=None):
    plan = resolve_plan(x_api_key)
    endpoints = []

    for row in read_access_matrix():
        endpoint = row.get("endpoint")
        endpoints.append({
            "endpoint": endpoint,
            "allowed": has_access(plan, endpoint),
            "free": str(row.get("free")).lower() == "true",
            "pro": str(row.get("pro")).lower() == "true",
            "enterprise": str(row.get("enterprise")).lower() == "true",
        })

    usage = [
        row for row in read_usage_records()
        if x_api_key and row.get("api_key") == x_api_key
    ]
    limit_status = build_limit_status(plan, usage) if plan else None

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "authenticated": plan is not None,
        "plan": plan,
        "allowed_endpoints": [
            row["endpoint"] for row in endpoints
            if row["allowed"]
        ],
        "endpoint_access": endpoints,
        "usage": {
            "total_calls": len(usage),
            "by_endpoint": summarize_usage_by_endpoint(usage),
            "recent": usage[-10:],
        },
        "limits": limit_status,
    }


def summarize_usage_by_endpoint(records):
    counts = {}
    for row in records:
        endpoint = row.get("endpoint", "unknown")
        counts[endpoint] = counts.get(endpoint, 0) + 1
    return [
        {"endpoint": endpoint, "calls": calls}
        for endpoint, calls in sorted(counts.items())
    ]


def build_usage_summary(x_api_key=None):
    records = [
        row for row in read_usage_records()
        if x_api_key and row.get("api_key") == x_api_key
    ]
    plan = resolve_plan(x_api_key)

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "plan": plan,
        "total_calls": len(records),
        "by_endpoint": summarize_usage_by_endpoint(records),
        "recent": records[-25:],
        "limits": build_limit_status(plan, records) if plan else None,
    }


def build_plan_limits():
    return {
        "product": "AI-RPCT",
        "version": "v1",
        "plans": read_plan_limits(),
    }


def enforce_plan_limits(plan, x_api_key):
    usage = [
        row for row in read_usage_records()
        if x_api_key and row.get("api_key") == x_api_key
    ]
    limit_status = build_limit_status(plan, usage)

    if limit_status["limited"]:
        raise HTTPException(
            status_code=429,
            detail={
                "allowed": False,
                "reason": limit_status["reason"],
                "plan": plan,
                "limits": limit_status["limits"],
                "daily_calls": limit_status["daily_calls"],
                "monthly_calls": limit_status["monthly_calls"],
                "daily_remaining": limit_status.get("daily_remaining", 0),
                "monthly_remaining": limit_status.get("monthly_remaining", 0),
            },
        )

    return limit_status


def require_v1_access(endpoint, x_api_key: str = Header(default=None)):
    plan = resolve_plan(x_api_key)

    if not has_access(plan, endpoint):
        raise HTTPException(
            status_code=403,
            detail={
                "allowed": False,
                "endpoint": endpoint,
                "required": "valid API key with sufficient plan",
                "current_plan": plan,
            },
        )

    limit_status = enforce_plan_limits(plan, x_api_key)
    log_usage(x_api_key, endpoint)

    return {
        "allowed": True,
        "plan": plan,
        "endpoint": endpoint,
        "limits": limit_status,
    }
