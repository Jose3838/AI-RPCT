from fastapi import APIRouter

from enterprise_report_index import build_enterprise_report_index
from sales_enterprise_bundle import build_sales_enterprise_bundle
from enterprise_access import require_enterprise
from coverage_milestone_report import build_coverage_milestone_report
from enterprise_intelligence_bundle_v2 import build_enterprise_intelligence_bundle_v2
from dynamic_entitlements import require_plan as require_dynamic_plan
from enterprise_decision_engine import build_enterprise_decision_engine

router = APIRouter()


@router.get("/enterprise-report-index")
def enterprise_report_index():
    return build_enterprise_report_index()


@router.get("/sales-enterprise-bundle")
def sales_enterprise_bundle():
    return build_sales_enterprise_bundle()


@router.get("/enterprise-sales-demo")
def enterprise_sales_demo(api_key: str):
    access = require_enterprise(api_key)

    if not access["allowed"]:
        return {
            "status": "blocked",
            **access
        }

    return {
        "status": "ok",
        "access": access,
        "bundle": build_sales_enterprise_bundle()
    }


@router.get("/coverage-milestone-report")
def coverage_milestone_report():
    return build_coverage_milestone_report()


@router.get("/enterprise-intelligence-bundle-v2")
def enterprise_intelligence_bundle_v2():
    return build_enterprise_intelligence_bundle_v2()


@router.get("/enterprise-intelligence-bundle-v2-gated")
def enterprise_intelligence_bundle_v2_gated(api_key: str):
    access = require_dynamic_plan(
        api_key,
        ["enterprise"]
    )

    if not access["allowed"]:
        return {
            "status": "blocked",
            **access
        }

    return {
        "status": "ok",
        "access": access,
        "bundle": build_enterprise_intelligence_bundle_v2()
    }


@router.get("/enterprise-decision-engine")
def enterprise_decision_engine():
    return build_enterprise_decision_engine()
