import os
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")

REQUIRED_PROVIDERS = [
    {"provider": "vast", "env_key": "VAST_API_KEY"},
    {"provider": "runpod", "env_key": "RUNPOD_API_KEY"},
]


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def build_provider_preflight(env=None, ingestion_rows=None):
    env = os.environ if env is None else env
    ingestion_rows = ingestion_rows if ingestion_rows is not None else read_records(
        DATA_DIR / "live_provider_ingestion_status.csv"
    )
    ingestion_by_provider = {
        row.get("provider"): row
        for row in ingestion_rows
    }

    rows = []
    for provider in REQUIRED_PROVIDERS:
        name = provider["provider"]
        env_key = provider["env_key"]
        configured = bool(env.get(env_key))
        ingestion = ingestion_by_provider.get(name, {})
        ingestion_status = ingestion.get("status", "not_run")
        used_fallback = as_bool(ingestion.get("used_fallback"))

        blockers = []
        if not configured:
            blockers.append("missing_api_key")
        if ingestion_status == "fallback" or used_fallback:
            blockers.append("using_fallback_data")
        if ingestion_status in {"empty", "error", "not_run"}:
            blockers.append("no_fresh_ingestion")

        if blockers:
            readiness = "blocked"
        elif ingestion_status == "fresh":
            readiness = "ready"
        else:
            readiness = "watch"

        rows.append({
            "provider": name,
            "env_key": env_key,
            "credential_configured": configured,
            "ingestion_status": ingestion_status,
            "used_fallback": used_fallback,
            "readiness": readiness,
            "blockers": ", ".join(blockers) if blockers else "none",
            "next_action": next_action_for(blockers, env_key),
        })

    return pd.DataFrame(rows)


def next_action_for(blockers, env_key):
    if "missing_api_key" in blockers:
        return f"Configure {env_key} in the runtime environment."
    if "using_fallback_data" in blockers:
        return "Restore fresh live ingestion and verify connector credentials."
    if "no_fresh_ingestion" in blockers:
        return "Run live provider ingestion and inspect connector errors."
    return "Maintain daily connector monitoring."


def summarize_provider_preflight(preflight):
    if preflight.empty:
        return {
            "provider_count": 0,
            "ready_count": 0,
            "blocked_count": 0,
            "paid_reliability_claims_allowed": False,
            "next_action": "Run provider preflight.",
        }

    blocked = preflight[preflight["readiness"] == "blocked"]
    ready = preflight[preflight["readiness"] == "ready"]
    return {
        "provider_count": int(len(preflight)),
        "ready_count": int(len(ready)),
        "blocked_count": int(len(blocked)),
        "paid_reliability_claims_allowed": len(blocked) == 0 and len(ready) == len(preflight),
        "next_action": blocked.iloc[0]["next_action"] if not blocked.empty else "Maintain daily connector monitoring.",
    }


def main():
    preflight = build_provider_preflight()
    DATA_DIR.mkdir(exist_ok=True)
    preflight.to_csv(DATA_DIR / "provider_preflight.csv", index=False)
    summary = summarize_provider_preflight(preflight)
    pd.DataFrame([summary]).to_csv(DATA_DIR / "provider_preflight_summary.csv", index=False)
    print(preflight)
    print(summary)


if __name__ == "__main__":
    main()
