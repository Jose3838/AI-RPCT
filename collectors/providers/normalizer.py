from __future__ import annotations


def normalize_provider_row(row: dict) -> dict:
    normalized = dict(row)

    normalized["provider"] = str(normalized.get("provider", "")).strip()
    normalized["gpu"] = str(normalized.get("gpu", "")).strip()

    normalized["price_per_hour"] = float(
        normalized.get("price_per_hour", 0) or 0
    )

    normalized["availability"] = int(
        float(normalized.get("availability", 0) or 0)
    )

    normalized["source"] = str(
        normalized.get("source", "provider_connector")
        or "provider_connector"
    ).strip()

    return normalized


def normalize_provider_rows(rows: list[dict]) -> list[dict]:
    return [
        normalize_provider_row(row)
        for row in rows
    ]
