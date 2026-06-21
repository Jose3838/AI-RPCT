from pathlib import Path
from datetime import datetime, timezone

from intelligence.reports.daily_intelligence_brief_v1 import (
    daily_intelligence_brief_v1
)

from intelligence.reports.weekly_market_report_v1 import (
    weekly_market_report_v1
)


REPORT_FILE = Path("data/reports/customer_report_v1.md")


def customer_report_export_v1():
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    daily = daily_intelligence_brief_v1()
    weekly = weekly_market_report_v1()

    content = f"""# AI-RPCT Customer Intelligence Report

Generated: {datetime.now(timezone.utc).isoformat()}

## Executive Summary

{weekly.get("summary")}

## Daily Brief

Headline: {daily.get("headline")}

Market Health: {daily.get("market_health")}
Data Moat: {daily.get("data_moat")}
Product Readiness: {daily.get("product_readiness")}
Executive Score: {daily.get("executive_score")}

## Customer Decision

{daily.get("customer_decision", {}).get("headline")}

## Weekly Market Report

{weekly.get("headline")}

{weekly.get("summary")}
"""

    REPORT_FILE.write_text(content)

    return {
        "status": "saved",
        "file": str(REPORT_FILE),
        "chars": len(content)
    }
