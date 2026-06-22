from html import escape
from pathlib import Path

from api.commercial_core import (
    build_account_health_snapshot,
    build_commercial_snapshot,
    build_revenue_forecast,
    build_sales_pipeline,
)


REPORTS_DIR = Path("reports")


def build_commercial_board_payload():
    commercial = build_commercial_snapshot()
    pipeline = build_sales_pipeline()
    health = build_account_health_snapshot()
    forecast = build_revenue_forecast()

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "commercial_board_export",
        "commercial": commercial,
        "pipeline": pipeline,
        "health": health,
        "forecast": forecast,
        "markdown": build_commercial_board_markdown(
            commercial,
            pipeline,
            health,
            forecast,
        ),
    }


def build_commercial_board_markdown(commercial, pipeline, health, forecast):
    commercial_summary = commercial["summary"]
    forecast_summary = forecast["summary"]
    lines = [
        "# AI-RPCT Commercial Board Report",
        "",
        "## Revenue Summary",
        f"- Current MRR: ${commercial_summary['mrr_usd']}",
        f"- Current ARR: ${commercial_summary['annual_run_rate_usd']}",
        f"- Expected MRR: ${forecast_summary['expected_mrr_usd']}",
        f"- Expected ARR: ${forecast_summary['expected_arr_usd']}",
        f"- Pipeline MRR Lift: ${forecast_summary['pipeline_mrr_lift_usd']}",
        f"- At-Risk MRR: ${forecast_summary['at_risk_mrr_usd']}",
        "",
        "## Pipeline",
        f"- Opportunities: {pipeline['summary']['opportunity_count']}",
        f"- Estimated MRR Lift: ${pipeline['summary']['estimated_mrr_lift_usd']}",
        f"- High Priority: {pipeline['summary']['high_priority']}",
        "",
        "## Account Health",
        f"- Accounts: {health['summary']['account_count']}",
        f"- At Risk: {health['summary']['at_risk']}",
        f"- Watch: {health['summary']['watch']}",
        "",
        "## Top Opportunities",
    ]

    for opportunity in pipeline["opportunities"][:5]:
        lines.extend([
            f"### {opportunity.get('customer_name', 'Unknown customer')}",
            f"- Type: {opportunity.get('opportunity_type', 'n/a')}",
            f"- Priority: {opportunity.get('priority', 'n/a')}",
            f"- Action: {opportunity.get('recommended_action', '')}",
            f"- Estimated MRR Lift: ${opportunity.get('estimated_mrr_lift_usd', 0)}",
            "",
        ])

    return "\n".join(lines)


def build_commercial_board_html():
    payload = build_commercial_board_payload()
    commercial = payload["commercial"]["summary"]
    pipeline = payload["pipeline"]["summary"]
    health = payload["health"]["summary"]
    forecast = payload["forecast"]["summary"]

    opportunities = "\n".join(
        f"""
        <section class="card">
          <div class="eyebrow">{escape(item.get('opportunity_type', 'opportunity'))} / {escape(item.get('priority', 'medium'))}</div>
          <h3>{escape(item.get('customer_name', 'Unknown customer'))}</h3>
          <p>{escape(item.get('recommended_action', ''))}</p>
          <strong>${escape(str(item.get('estimated_mrr_lift_usd', 0)))} MRR lift</strong>
        </section>
        """
        for item in payload["pipeline"]["opportunities"][:6]
    ) or "<p>No active sales opportunities.</p>"

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI-RPCT Commercial Board Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #111827; }}
    h1 {{ margin-bottom: 4px; }}
    h2 {{ margin-top: 32px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; }}
    .meta {{ color: #6b7280; margin-bottom: 28px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
    .metric, .card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 12px; }}
    .metric strong {{ display: block; font-size: 22px; margin-top: 6px; }}
    .eyebrow {{ color: #2563eb; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    @media print {{ body {{ margin: 24px; }} }}
  </style>
</head>
<body>
  <h1>AI-RPCT Commercial Board Report</h1>
  <div class="meta">Enterprise commercial snapshot for AI-RPCT</div>

  <h2>Revenue Forecast</h2>
  <div class="metrics">
    <div class="metric">Current MRR<strong>${escape(str(commercial['mrr_usd']))}</strong></div>
    <div class="metric">Current ARR<strong>${escape(str(commercial['annual_run_rate_usd']))}</strong></div>
    <div class="metric">Expected MRR<strong>${escape(str(forecast['expected_mrr_usd']))}</strong></div>
    <div class="metric">Expected ARR<strong>${escape(str(forecast['expected_arr_usd']))}</strong></div>
    <div class="metric">Pipeline Lift<strong>${escape(str(forecast['pipeline_mrr_lift_usd']))}</strong></div>
    <div class="metric">At-Risk MRR<strong>${escape(str(forecast['at_risk_mrr_usd']))}</strong></div>
    <div class="metric">Opportunities<strong>{escape(str(pipeline['opportunity_count']))}</strong></div>
    <div class="metric">At-Risk Accounts<strong>{escape(str(health['at_risk']))}</strong></div>
  </div>

  <h2>Top Opportunities</h2>
  {opportunities}
</body>
</html>
"""


def save_commercial_board_report():
    REPORTS_DIR.mkdir(exist_ok=True)
    html_path = REPORTS_DIR / "commercial_board_report_v1.html"
    markdown_path = REPORTS_DIR / "commercial_board_report_v1.md"
    payload = build_commercial_board_payload()

    html_path.write_text(build_commercial_board_html())
    markdown_path.write_text(payload["markdown"])

    return {
        "status": "ok",
        "html_file": str(html_path),
        "markdown_file": str(markdown_path),
        "payload": payload,
    }
