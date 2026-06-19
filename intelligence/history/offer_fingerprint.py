import hashlib

def build_offer_fingerprint(
    provider,
    gpu_model,
    region,
    price=None
):
    raw = (
        f"{provider}|"
        f"{gpu_model}|"
        f"{region}|"
        f"{price}"
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()[:16]
