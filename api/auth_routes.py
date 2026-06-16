from fastapi import APIRouter, Header, HTTPException

from security.api_keys import (
    validate_api_key
)

router = APIRouter()

@router.get("/protected")
def protected(
    x_api_key: str = Header(None)
):
    if not validate_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return {
        "access": "granted"
    }

@router.get("/my-plan")
def my_plan(
    x_api_key: str = Header(None)
):
    from security.plans import get_plan_for_key

    plan = get_plan_for_key(x_api_key)

    if plan is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return {
        "plan": plan
    }

@router.get("/tracked")
def tracked(
    x_api_key: str = Header(None)
):
    from security.api_keys import validate_api_key
    from security.usage import log_usage

    if not validate_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    log_usage(x_api_key, "/tracked")

    return {
        "status": "tracked"
    }

@router.get("/users")
def users():
    from security.users import get_users
    return get_users()
