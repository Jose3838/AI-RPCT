import os
from dotenv import load_dotenv


load_dotenv()


REQUIRED_KEYS = {
    "vast": "VAST_API_KEY",
    "runpod": "RUNPOD_API_KEY",
    "coreweave": "COREWEAVE_API_KEY",
    "lambda": "LAMBDA_API_KEY",
    "nebius": "NEBIUS_API_KEY",
    "crusoe": "CRUSOE_API_KEY"
}


def build_provider_api_key_readiness():
    results = []

    for provider, env_key in REQUIRED_KEYS.items():
        value = os.getenv(env_key)

        results.append({
            "provider": provider,
            "env_key": env_key,
            "configured": bool(value)
        })

    configured = len([
        item for item in results
        if item["configured"]
    ])

    total = len(results)

    return {
        "status": "ok",
        "version": "v1",
        "configured_keys": configured,
        "required_keys": total,
        "api_key_readiness_percentage": round((configured / total) * 100, 2),
        "providers": results
    }
