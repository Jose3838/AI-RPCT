import json
import os
from pathlib import Path

import pandas as pd

from analytics.provider_preflight import REQUIRED_PROVIDERS, is_configured_secret


DATA_DIR = Path("data")

PROVIDER_SETUP = {
    "vast": {
        "account_step": "Create or open a Vast.ai account and generate an API key.",
        "docs": "docs/VAST_INTEGRATION.md",
        "verification_command": "./scripts/run_core_intelligence.sh",
    },
    "runpod": {
        "account_step": "Create or open a RunPod account and generate an API key.",
        "docs": "docs/REAL_PROVIDER_REQUIREMENTS.md",
        "verification_command": "./scripts/run_core_intelligence.sh",
    },
}


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def by_provider(records):
    return {
        str(row.get("provider", "")).strip().lower(): row
        for row in records
        if row.get("provider")
    }


def provider_recovery_step(provider, env, preflight_row, ingestion_row):
    name = provider["provider"]
    env_key = provider["env_key"]
    setup = PROVIDER_SETUP.get(name, {})
    configured = is_configured_secret(env.get(env_key))
    preflight_readiness = str(preflight_row.get("readiness", "unknown")).lower()
    ingestion_status = str(ingestion_row.get("status", preflight_row.get("ingestion_status", "unknown"))).lower()
    used_fallback = str(ingestion_row.get("used_fallback", preflight_row.get("used_fallback", False))).lower() in {
        "true",
        "1",
        "yes",
    }

    if not configured:
        status = "missing_credential"
        next_action = f"Set {env_key} in .env or the runtime environment."
    elif ingestion_status in {"fallback", "empty", "error", "not_run", "unknown"} or used_fallback:
        status = "credential_needs_ingestion_verification"
        next_action = "Run the core intelligence pipeline and inspect live provider ingestion status."
    elif preflight_readiness == "ready" and ingestion_status == "fresh":
        status = "verified_live"
        next_action = "Maintain daily connector monitoring."
    else:
        status = "watch"
        next_action = preflight_row.get("next_action", "Verify provider connector output.")

    return {
        "provider": name,
        "env_key": env_key,
        "status": status,
        "credential_configured": configured,
        "preflight_readiness": preflight_readiness,
        "ingestion_status": ingestion_status,
        "used_fallback": used_fallback,
        "account_step": setup.get("account_step", f"Generate an API key for {name}."),
        "env_step": f"Add {env_key}=... to .env or export {env_key} in the shell.",
        "verification_command": setup.get("verification_command", "./scripts/run_core_intelligence.sh"),
        "docs": setup.get("docs", ""),
        "next_action": next_action,
    }


def build_provider_recovery_plan(env=None, data_dir=DATA_DIR):
    env = os.environ if env is None else env
    data_dir = Path(data_dir)
    preflight = by_provider(read_records(data_dir / "provider_preflight.csv"))
    ingestion = by_provider(read_records(data_dir / "live_provider_ingestion_status.csv"))

    providers = [
        provider_recovery_step(
            provider,
            env,
            preflight.get(provider["provider"], {}),
            ingestion.get(provider["provider"], {}),
        )
        for provider in REQUIRED_PROVIDERS
    ]

    missing = [item for item in providers if item["status"] == "missing_credential"]
    verification = [
        item for item in providers
        if item["status"] == "credential_needs_ingestion_verification"
    ]
    verified = [item for item in providers if item["status"] == "verified_live"]

    if missing:
        status = "blocked_by_missing_credentials"
        next_action = missing[0]["next_action"]
    elif verification:
        status = "blocked_by_ingestion_verification"
        next_action = verification[0]["next_action"]
    elif len(verified) == len(providers):
        status = "ready_for_clean_history_collection"
        next_action = "Run the core pipeline daily until 30 clean history days are collected."
    else:
        status = "watch"
        next_action = providers[0]["next_action"] if providers else "Run provider preflight."

    return {
        "product": "AI-RPCT",
        "report_type": "provider_recovery_plan",
        "status": status,
        "required_provider_count": len(providers),
        "configured_count": len([item for item in providers if item["credential_configured"]]),
        "verified_live_count": len(verified),
        "missing_credentials": [item["env_key"] for item in missing],
        "next_action": next_action,
        "safe_to_print": True,
        "providers": providers,
    }


def main():
    print(json.dumps(build_provider_recovery_plan(), indent=2))


if __name__ == "__main__":
    main()
