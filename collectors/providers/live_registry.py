import os

def use_vast_real():
    return bool(os.getenv("VAST_API_KEY"))
