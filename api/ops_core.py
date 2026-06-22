from pathlib import Path

import pandas as pd


def read_latest_record(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    records = pd.read_csv(path).to_dict(orient="records")
    return records[-1] if records else {}


def file_status(path):
    path = Path(path)
    return {
        "path": str(path),
        "exists": path.exists(),
        "non_empty": path.exists() and path.stat().st_size > 1,
    }


def read_launch_controls():
    path = Path("data/launch_controls.csv")
    if not path.exists() or path.stat().st_size <= 1:
        return {}

    controls = {}
    for row in pd.read_csv(path).to_dict(orient="records"):
        control = row.get("control")
        if not control:
            continue
        controls[str(control).strip()] = {
            "status": str(row.get("status", "")).strip().lower() == "true",
            "detail": str(row.get("detail", "") or ""),
        }
    return controls


def build_v1_operations_status():
    required_files = [
        "data/api_key_registry.csv",
        "data/customer_accounts.csv",
        "data/plan_access_matrix.csv",
        "data/plan_limits.csv",
        "data/plan_pricing.csv",
        "data/launch_controls.csv",
        "api/terminal_core.py",
        "api/access.py",
        "api/commercial_core.py",
        "api/onboarding_core.py",
        "api/audit_core.py",
        "web/index.html",
        "web/app.js",
    ]
    files = [file_status(path) for path in required_files]
    missing = [item["path"] for item in files if not item["exists"]]
    empty = [item["path"] for item in files if item["exists"] and not item["non_empty"]]

    product = read_latest_record("data/product_readiness_score.csv")
    monetization = read_latest_record("data/monetization_readiness.csv")
    commercial = read_latest_record("data/commercial_readiness.csv")
    beta = read_latest_record("data/public_beta_status.csv")
    launch_controls = read_launch_controls()

    blocking_issues = []
    if missing:
        blocking_issues.append("required_files_missing")
    if empty:
        blocking_issues.append("required_files_empty")
    paid_allowed = launch_controls.get("paid_customers_allowed", {}).get(
        "status",
        str(beta.get("paid_customers_allowed", "False")).lower() == "true",
    )
    billing_ready = launch_controls.get("billing_ready", {}).get(
        "status",
        str(commercial.get("billing_ready", "False")).lower() == "true",
    )
    terms_ready = launch_controls.get("terms_ready", {}).get(
        "status",
        str(commercial.get("terms_ready", "False")).lower() == "true",
    )

    if not paid_allowed:
        blocking_issues.append("paid_customers_not_enabled")
    if not billing_ready:
        blocking_issues.append("billing_not_ready")
    if not terms_ready:
        blocking_issues.append("terms_not_ready")

    status = "ready" if not blocking_issues else "beta_watch"

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "operations_status",
        "status": status,
        "blocking_issues": blocking_issues,
        "readiness": {
            "product": product,
            "monetization": monetization,
            "commercial": commercial,
            "public_beta": beta,
            "launch_controls": launch_controls,
        },
        "files": files,
    }


def build_launch_controls():
    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "launch_controls",
        "controls": read_launch_controls(),
    }
