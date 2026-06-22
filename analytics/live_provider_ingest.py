from pathlib import Path

import pandas as pd

from collectors.providers.runpod_real import RunPodRealProvider
from collectors.providers.vast_real import VastRealProvider


DATA_DIR = Path("data")
OUTPUT_COLUMNS = [
    "provider",
    "gpu",
    "price_per_hour",
    "availability",
    "timestamp",
]


def normalize_provider_name(provider):
    provider = str(provider).strip().lower()
    if provider.endswith("_real"):
        provider = provider[:-5]
    return provider


def provider_output_file(provider_name):
    provider_name = normalize_provider_name(provider_name)
    if provider_name == "vast":
        return DATA_DIR / "vast_live_report.csv"
    if provider_name == "runpod":
        return DATA_DIR / "runpod_live_report.csv"
    return DATA_DIR / f"{provider_name}_live_report.csv"


def rows_to_frame(rows):
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    for column in OUTPUT_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df = df[OUTPUT_COLUMNS].copy()
    df["provider"] = df["provider"].map(normalize_provider_name)
    df["price_per_hour"] = pd.to_numeric(df["price_per_hour"], errors="coerce").fillna(0)
    df["availability"] = pd.to_numeric(df["availability"], errors="coerce").fillna(0)
    return df


def fetch_provider(provider):
    provider_name = normalize_provider_name(getattr(provider, "name", provider.__class__.__name__))
    output_file = provider_output_file(provider_name)
    status = {
        "provider": provider_name,
        "status": "empty",
        "fresh_rows": 0,
        "used_fallback": False,
        "output_file": str(output_file),
        "error": "",
    }

    try:
        fresh = rows_to_frame(provider.fetch())
    except Exception as exc:
        fresh = pd.DataFrame(columns=OUTPUT_COLUMNS)
        status["status"] = "error"
        status["error"] = type(exc).__name__

    if not fresh.empty:
        status["status"] = "fresh"
        status["fresh_rows"] = len(fresh)
        return fresh, status

    if output_file.exists() and output_file.stat().st_size > 1:
        fallback = rows_to_frame(pd.read_csv(output_file).to_dict(orient="records"))
        status["status"] = "fallback"
        status["used_fallback"] = True
        return fallback, status

    return pd.DataFrame(columns=OUTPUT_COLUMNS), status


def run_live_provider_ingest(providers=None):
    providers = providers or [VastRealProvider(), RunPodRealProvider()]
    DATA_DIR.mkdir(exist_ok=True)

    frames = []
    statuses = []

    for provider in providers:
        df, status = fetch_provider(provider)
        statuses.append(status)

        output_file = Path(status["output_file"])
        df.to_csv(output_file, index=False)

        if not df.empty:
            frames.append(df)

    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=OUTPUT_COLUMNS)
    combined.to_csv(DATA_DIR / "live_provider_data.csv", index=False)

    status_df = pd.DataFrame(statuses)
    status_df.to_csv(DATA_DIR / "live_provider_ingestion_status.csv", index=False)

    return {
        "providers": len(statuses),
        "fresh_providers": int((status_df["status"] == "fresh").sum()) if not status_df.empty else 0,
        "fallback_providers": int(status_df["used_fallback"].sum()) if not status_df.empty else 0,
        "rows": int(len(combined)),
        "statuses": statuses,
    }


def main():
    result = run_live_provider_ingest()
    print(result)


if __name__ == "__main__":
    main()
