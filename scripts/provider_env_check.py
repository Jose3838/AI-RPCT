import json
import os

from analytics.provider_preflight import REQUIRED_PROVIDERS, is_configured_secret


def build_provider_env_check(env=None):
    env = os.environ if env is None else env
    providers = []

    for provider in REQUIRED_PROVIDERS:
        env_key = provider["env_key"]
        configured = is_configured_secret(env.get(env_key))
        providers.append({
            "provider": provider["provider"],
            "env_key": env_key,
            "credential_status": "configured" if configured else "missing_or_placeholder",
            "configured": configured,
            "safe_to_print": True,
        })

    configured_count = len([item for item in providers if item["configured"]])
    return {
        "product": "AI-RPCT",
        "configured_count": configured_count,
        "required_count": len(providers),
        "all_required_configured": configured_count == len(providers),
        "providers": providers,
        "next_action": (
            "Run ./scripts/run_core_intelligence.sh"
            if configured_count == len(providers)
            else "Copy .env.example to .env and configure VAST_API_KEY and RUNPOD_API_KEY."
        ),
    }


def main():
    print(json.dumps(build_provider_env_check(), indent=2))


if __name__ == "__main__":
    main()
