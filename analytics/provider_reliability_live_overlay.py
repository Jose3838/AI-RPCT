from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "provider_reliability_live_overlay.csv"


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def read_table(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize_provider(provider):
    provider = str(provider or "").strip().lower()
    if provider.endswith("_real"):
        provider = provider[:-5]
    if provider == "lambda":
        return "lambda_labs"
    return provider


def build_provider_reliability_live_overlay():
    ranking = read_table(DATA_DIR / "provider_reliability_ranking.csv")
    ingestion = read_table(DATA_DIR / "live_provider_ingestion_status.csv")
    preflight = read_table(DATA_DIR / "provider_preflight.csv")

    if ranking.empty:
        return pd.DataFrame([{
            "provider": "",
            "reliability_score": 0,
            "reliability_band": "missing",
            "live_ingestion_status": "missing",
            "used_fallback": True,
            "preflight_readiness": "missing",
            "live_reliability_ready": False,
            "blockers": "missing_provider_reliability_ranking",
        }])

    ranking = ranking.copy()
    ranking["provider_key"] = ranking["provider"].map(normalize_provider)
    ingestion_by_provider = {}
    preflight_by_provider = {}

    if not ingestion.empty:
        ingestion["provider_key"] = ingestion["provider"].map(normalize_provider)
        ingestion_by_provider = ingestion.drop_duplicates("provider_key", keep="last").set_index("provider_key").to_dict(orient="index")
    if not preflight.empty:
        preflight["provider_key"] = preflight["provider"].map(normalize_provider)
        preflight_by_provider = preflight.drop_duplicates("provider_key", keep="last").set_index("provider_key").to_dict(orient="index")

    rows = []
    for _, row in ranking.iterrows():
        provider_key = row.get("provider_key")
        ingestion_row = ingestion_by_provider.get(provider_key, {})
        preflight_row = preflight_by_provider.get(provider_key, {})
        live_status = str(ingestion_row.get("status", row.get("ingestion_status", "unknown"))).lower()
        used_fallback = as_bool(ingestion_row.get("used_fallback", row.get("used_fallback", False)))
        preflight_readiness = str(preflight_row.get("readiness", "unknown")).lower()
        blockers = []
        if live_status != "fresh":
            blockers.append("live_ingestion_not_fresh")
        if used_fallback:
            blockers.append("provider_using_fallback")
        if preflight_readiness == "blocked":
            blockers.append("provider_preflight_blocked")
        if float(row.get("history_days", 0)) < 30:
            blockers.append("insufficient_reliability_history")

        rows.append({
            "provider": row.get("provider"),
            "reliability_score": row.get("reliability_score"),
            "reliability_band": row.get("reliability_band"),
            "live_ingestion_status": live_status,
            "used_fallback": used_fallback,
            "preflight_readiness": preflight_readiness,
            "history_days": row.get("history_days", 0),
            "live_reliability_ready": not blockers,
            "blockers": ", ".join(blockers) if blockers else "none",
        })

    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_provider_reliability_live_overlay()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
