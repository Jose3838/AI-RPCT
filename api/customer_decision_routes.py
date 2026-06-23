from fastapi import APIRouter
from analytics.customer_decision_layer import build_customer_decision_brief

router = APIRouter()

@router.get("/v1/customer-decision-brief")
def customer_decision_brief():
    return build_customer_decision_brief()

from fastapi.responses import PlainTextResponse
from analytics.customer_decision_layer import build_customer_decision_markdown

@router.get("/v1/customer-decision-brief/markdown", response_class=PlainTextResponse)
def customer_decision_brief_markdown():
    return build_customer_decision_markdown()
