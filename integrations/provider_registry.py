PROVIDERS = {
    "runpod": True,
    "vast": True,
    "lambda": True,
    "coreweave": True
}

def active_providers():
    return [
        k for k, v in PROVIDERS.items()
        if v
    ]
