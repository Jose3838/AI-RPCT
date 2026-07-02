from fastapi import APIRouter

from organizations import create_organization, list_organizations
from api_key_management import create_api_key, list_api_keys
from organization_revenue_dashboard import build_organization_revenue_dashboard
from organization_usage_dashboard import build_organization_usage_dashboard

router = APIRouter()


@router.post("/create-organization")
def create_organization_endpoint(
    name: str,
    plan: str,
    api_key: str
):
    return create_organization(
        name,
        plan,
        api_key
    )


@router.get("/organizations")
def organizations_endpoint():
    return {
        "status": "ok",
        "organizations": list_organizations()
    }


@router.post("/create-api-key")
def create_api_key_endpoint(
    organization_id: int,
    plan: str
):
    return create_api_key(
        organization_id,
        plan
    )


@router.get("/api-keys")
def api_keys_endpoint():
    return {
        "status": "ok",
        "api_keys": list_api_keys()
    }


@router.get("/organization-revenue-dashboard")
def organization_revenue_dashboard():
    return build_organization_revenue_dashboard()


@router.get("/organization-usage-dashboard")
def organization_usage_dashboard():
    return build_organization_usage_dashboard()
