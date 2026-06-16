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
