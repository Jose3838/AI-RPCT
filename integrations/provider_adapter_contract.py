REQUIRED_PROVIDER_FIELDS = [
    "provider",
    "gpu",
    "price_per_hour",
    "availability",
    "timestamp"
]

def validate_adapter_output(rows):
    errors = []

    if not isinstance(rows, list):
        return ["Provider output must be a list"]

    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"Row {i} is not a dictionary")
            continue

        for field in REQUIRED_PROVIDER_FIELDS:
            if field not in row:
                errors.append(f"Row {i} missing field: {field}")

    return errors
