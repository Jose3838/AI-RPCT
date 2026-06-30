from __future__ import annotations

from copilot.dashboard_executive import get_executive_dashboard


def get_dashboard() -> dict:
    dashboard = get_executive_dashboard()

    return {
        "status": "dashboard available",
        "generated_by": "AI-RPCT Dashboard Service",
        "version": "1.0",
        "dashboard": dashboard,
    }
