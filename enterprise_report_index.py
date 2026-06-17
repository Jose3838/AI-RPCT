from weekly_infrastructure_report import build_weekly_infrastructure_report


def build_enterprise_report_index():
    report = build_weekly_infrastructure_report()

    return {
        "status": "ok",
        "version": "v1",
        "product": "AI-RPCT",
        "report_type": "enterprise_report_index",
        "commercial_signal": "enterprise_ready",
        "data_moat_status": "growing",
        "monetization_priority": "high",
        "weekly_report": report
    }
