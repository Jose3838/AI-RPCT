from pathlib import Path
import re
import secrets

import pandas as pd
from fastapi import HTTPException


API_KEY_REGISTRY_FILE = Path("data/api_key_registry.csv")
CUSTOMER_ACCOUNTS_FILE = Path("data/customer_accounts.csv")
VALID_PLANS = {"free", "pro", "enterprise"}


def read_csv_records(path, columns):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path)


def write_csv_records(path, frame):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def make_account_id(customer_name):
    slug = re.sub(r"[^a-z0-9]+", "_", customer_name.lower()).strip("_")
    suffix = secrets.token_hex(3)
    return f"acct_{slug or 'customer'}_{suffix}"


def create_customer_api_key(customer_name, plan):
    customer_name = str(customer_name or "").strip()
    plan = str(plan or "").strip().lower()

    if not customer_name:
        raise HTTPException(status_code=400, detail="customer_name is required")

    if plan not in VALID_PLANS:
        raise HTTPException(
            status_code=400,
            detail=f"plan must be one of: {', '.join(sorted(VALID_PLANS))}",
        )

    registry = read_csv_records(
        API_KEY_REGISTRY_FILE,
        ["key", "plan", "status"],
    )
    accounts = read_csv_records(
        CUSTOMER_ACCOUNTS_FILE,
        ["account_id", "customer_name", "api_key", "plan", "status"],
    )

    api_key = f"airpct_{secrets.token_hex(16)}"
    account_id = make_account_id(customer_name)

    registry = pd.concat([
        registry,
        pd.DataFrame([{
            "key": api_key,
            "plan": plan,
            "status": "active",
        }]),
    ], ignore_index=True)
    accounts = pd.concat([
        accounts,
        pd.DataFrame([{
            "account_id": account_id,
            "customer_name": customer_name,
            "api_key": api_key,
            "plan": plan,
            "status": "active",
        }]),
    ], ignore_index=True)

    write_csv_records(API_KEY_REGISTRY_FILE, registry)
    write_csv_records(CUSTOMER_ACCOUNTS_FILE, accounts)

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "status": "created",
        "account": {
            "account_id": account_id,
            "customer_name": customer_name,
            "plan": plan,
            "status": "active",
        },
        "api_key": api_key,
    }


def update_customer_api_key_status(api_key, status):
    api_key = str(api_key or "").strip()
    status = str(status or "").strip().lower()

    if not api_key:
        raise HTTPException(status_code=400, detail="api_key is required")

    if status not in {"active", "revoked"}:
        raise HTTPException(status_code=400, detail="status must be active or revoked")

    registry = read_csv_records(
        API_KEY_REGISTRY_FILE,
        ["key", "plan", "status"],
    )
    accounts = read_csv_records(
        CUSTOMER_ACCOUNTS_FILE,
        ["account_id", "customer_name", "api_key", "plan", "status"],
    )

    registry_match = registry["key"] == api_key
    account_match = accounts["api_key"] == api_key

    if registry.empty or not registry_match.any():
        raise HTTPException(status_code=404, detail="api key not found")

    registry.loc[registry_match, "status"] = status
    if not accounts.empty and account_match.any():
        accounts.loc[account_match, "status"] = status

    write_csv_records(API_KEY_REGISTRY_FILE, registry)
    write_csv_records(CUSTOMER_ACCOUNTS_FILE, accounts)

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "status": "updated",
        "api_key": api_key,
        "key_status": status,
    }


def revoke_customer_api_key(api_key):
    return update_customer_api_key_status(api_key, "revoked")


def reactivate_customer_api_key(api_key):
    return update_customer_api_key_status(api_key, "active")
