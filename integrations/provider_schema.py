REQUIRED_FIELDS = [
    "provider",
    "gpu",
    "price_per_hour",
    "availability"
]

def validate_provider_rows(rows):
    errors = []

    for index, row in enumerate(rows):
        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(
                    f"Row {index} missing field: {field}"
                )

    return errors
