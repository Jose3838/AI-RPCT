from fastapi import APIRouter

from billing_engine import build_billing_summary
from invoice_generator import generate_invoices
from revenue_dashboard import build_revenue_dashboard

router = APIRouter()


@router.get("/billing-summary")
def billing_summary():
    return {
        "status": "ok",
        "billing": build_billing_summary()
    }


@router.get("/invoice-summary")
def invoice_summary():
    return {
        "status": "ok",
        "invoices": generate_invoices()
    }


@router.get("/revenue-dashboard")
def revenue_dashboard():
    return build_revenue_dashboard()
