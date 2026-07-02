from fastapi import APIRouter

from usage_tracking import track_usage
from usage_analytics import get_usage_analytics
from dynamic_entitlements import get_plan_for_api_key, require_plan
from data_trust_index import build_data_trust_index

router = APIRouter()


@router.get("/usage-test")
def usage_test(api_key: str = "demo-free-key"):

    track_usage(
        api_key,
        "/usage-test"
    )

    return {
        "status": "tracked"
    }


@router.get("/usage-analytics-v2")
def usage_analytics_v2():
    return {
        "status": "ok",
        "usage": get_usage_analytics()
    }


@router.get("/entitlement-check-v2")
def entitlement_check_v2(api_key: str):
    return {
        "status": "ok",
        "api_key": api_key,
        "plan": get_plan_for_api_key(api_key)
    }


@router.get("/enterprise-check-v2")
def enterprise_check_v2(api_key: str):
    return require_plan(
        api_key,
        ["enterprise"]
    )


@router.get("/data-trust-index")
def data_trust_index():
    return build_data_trust_index()
