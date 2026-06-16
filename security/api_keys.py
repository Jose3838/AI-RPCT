VALID_KEYS = [
    "demo-key"
]

def validate_api_key(key):
    return key in VALID_KEYS
