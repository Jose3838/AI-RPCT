import os

DEFAULT_KEYS = "demo-key"

VALID_KEYS = [
    key.strip()
    for key in os.environ.get("AI_RPCT_API_KEYS", DEFAULT_KEYS).split(",")
    if key.strip()
]


def validate_api_key(key):
    if not key:
        return False
    return key in VALID_KEYS
