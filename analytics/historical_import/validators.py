from __future__ import annotations

REQUIRED_FIELDS = {
    "gpu_releases": ["release_date", "gpu", "vendor", "architecture"],
    "market_events": ["date", "event_name", "event_type", "impact_area"],
    "provider_pricing": ["date", "provider", "gpu", "price_per_hour"],
}


def validate_rows(rows: list[dict], category: str) -> list[str]:
    errors = []
    required = REQUIRED_FIELDS.get(category, [])

    for index, row in enumerate(rows):
        for field in required:
            if field not in row or row[field] in {None, ""}:
                errors.append(f"row={index} missing field={field}")

    return errors
