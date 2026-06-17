API_KEYS = {
    "demo-free-key": "free",
    "demo-pro-key": "pro",
    "demo-enterprise-key": "enterprise"
}


def get_plan_from_api_key(api_key):
    return API_KEYS.get(api_key, "unknown")


def require_enterprise(api_key):
    plan = get_plan_from_api_key(api_key)

    if plan != "enterprise":
        return {
            "allowed": False,
            "plan": plan,
            "error": "enterprise_plan_required"
        }

    return {
        "allowed": True,
        "plan": plan
    }
