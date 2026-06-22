from html import escape
from pathlib import Path

from api.terminal_core import (
    build_executive_brief,
    build_market_signals,
    build_recommendations,
)


REPORTS_DIR = Path("reports")


def _evidence_text(evidence):
    if not evidence:
        return "No evidence attached."

    parts = []
    for key, value in evidence.items():
        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        parts.append(f"{key}: {value}")
    return " | ".join(parts)


def build_customer_report_payload(customer_name="AI Infrastructure Buyer"):
    brief = build_executive_brief()
    signals = build_market_signals()["signals"]
    recommendations = build_recommendations()["recommendations"]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "customer_report_pdf_ready",
        "customer_name": customer_name,
        "headline": brief["headline"],
        "summary": brief["summary"],
        "core_metrics": brief["core_metrics"],
        "signals": signals,
        "recommendations": recommendations,
        "markdown": build_customer_report_markdown(
            customer_name,
            brief,
            signals,
            recommendations,
        ),
    }


def build_customer_report_markdown(customer_name, brief, signals, recommendations):
    metrics = brief["core_metrics"]
    lines = [
        "# AI-RPCT Customer Intelligence Report",
        "",
        f"Customer: {customer_name}",
        f"Generated: {brief['generated_at']}",
        "",
        "## Executive Summary",
        brief["headline"],
        "",
        brief["summary"],
        "",
        "## Core Metrics",
        f"- AI Infrastructure Index: {metrics.get('ai_infrastructure_index', 'n/a')}",
        f"- GPU Price Index: {metrics.get('gpu_price_index', 'n/a')}",
        f"- GPU Price Trend: {metrics.get('gpu_price_trend', 'n/a')}",
        f"- Terminal Risk Score: {metrics.get('terminal_risk_score', 'n/a')}",
        f"- Risk Level: {metrics.get('risk_level', 'n/a')}",
        f"- Top Provider: {metrics.get('top_provider', 'n/a')}",
        f"- Live Data Quality Score: {metrics.get('live_data_quality_score', 'n/a')}",
        "",
        "## Decision Signals",
    ]

    for signal in signals:
        lines.extend([
            f"### {signal.get('title', 'Untitled signal')}",
            f"- Type: {signal.get('type', 'n/a')}",
            f"- Severity: {signal.get('severity', 'n/a')}",
            f"- Message: {signal.get('message', '')}",
            f"- Evidence: {_evidence_text(signal.get('evidence', {}))}",
            "",
        ])

    lines.append("## Recommended Actions")

    for recommendation in recommendations:
        lines.extend([
            f"### {recommendation.get('title', 'Untitled recommendation')}",
            f"- Action: {recommendation.get('action', 'n/a')}",
            f"- Priority: {recommendation.get('priority', 'n/a')}",
            f"- Rationale: {recommendation.get('rationale', '')}",
            f"- Evidence: {_evidence_text(recommendation.get('evidence', {}))}",
            "",
        ])

    lines.extend([
        "## Notes",
        "This report is generated from AI-RPCT terminal data. Provider API keys and live-data freshness should be reviewed before using this report for contractual purchase decisions.",
    ])

    return "\n".join(lines)


def build_customer_report_html(customer_name="AI Infrastructure Buyer"):
    payload = build_customer_report_payload(customer_name)
    metrics = payload["core_metrics"]

    signal_cards = "\n".join(
        f"""
        <section class="card">
          <div class="eyebrow">{escape(signal.get('type', 'signal'))} / {escape(signal.get('severity', 'n/a'))}</div>
          <h3>{escape(signal.get('title', 'Untitled signal'))}</h3>
          <p>{escape(signal.get('message', ''))}</p>
          <small>{escape(_evidence_text(signal.get('evidence', {})))}</small>
        </section>
        """
        for signal in payload["signals"]
    )

    recommendation_cards = "\n".join(
        f"""
        <section class="card">
          <div class="eyebrow">{escape(recommendation.get('action', 'recommendation'))} / {escape(recommendation.get('priority', 'n/a'))}</div>
          <h3>{escape(recommendation.get('title', 'Untitled recommendation'))}</h3>
          <p>{escape(recommendation.get('rationale', ''))}</p>
          <small>{escape(_evidence_text(recommendation.get('evidence', {})))}</small>
        </section>
        """
        for recommendation in payload["recommendations"]
    )

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI-RPCT Customer Intelligence Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #111827; }}
    h1 {{ margin-bottom: 4px; }}
    h2 {{ margin-top: 32px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; }}
    .meta {{ color: #6b7280; margin-bottom: 28px; }}
    .summary {{ font-size: 18px; line-height: 1.5; background: #f3f4f6; padding: 20px; border-radius: 8px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .metric, .card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 12px; }}
    .metric strong {{ display: block; font-size: 22px; margin-top: 6px; }}
    .eyebrow {{ color: #2563eb; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    small {{ color: #6b7280; }}
    @media print {{ body {{ margin: 24px; }} }}
  </style>
</head>
<body>
  <h1>AI-RPCT Customer Intelligence Report</h1>
  <div class="meta">Customer: {escape(payload["customer_name"])} | Generated: {escape(build_executive_brief()["generated_at"])}</div>

  <h2>Executive Summary</h2>
  <div class="summary">
    <strong>{escape(payload["headline"])}</strong>
    <p>{escape(payload["summary"])}</p>
  </div>

  <h2>Core Metrics</h2>
  <div class="metrics">
    <div class="metric">AI Infrastructure Index<strong>{escape(str(metrics.get("ai_infrastructure_index", "n/a")))}</strong></div>
    <div class="metric">GPU Price Index<strong>{escape(str(metrics.get("gpu_price_index", "n/a")))}</strong></div>
    <div class="metric">Terminal Risk Score<strong>{escape(str(metrics.get("terminal_risk_score", "n/a")))}</strong></div>
    <div class="metric">Risk Level<strong>{escape(str(metrics.get("risk_level", "n/a")))}</strong></div>
    <div class="metric">Top Provider<strong>{escape(str(metrics.get("top_provider", "n/a")))}</strong></div>
    <div class="metric">Data Quality<strong>{escape(str(metrics.get("live_data_quality_score", "n/a")))}</strong></div>
  </div>

  <h2>Decision Signals</h2>
  {signal_cards}

  <h2>Recommended Actions</h2>
  {recommendation_cards}
</body>
</html>
"""


def save_customer_report(customer_name="AI Infrastructure Buyer"):
    REPORTS_DIR.mkdir(exist_ok=True)
    safe_name = customer_name.lower().replace(" ", "_").replace("/", "_")
    html_path = REPORTS_DIR / f"customer_report_{safe_name}_v1.html"
    markdown_path = REPORTS_DIR / f"customer_report_{safe_name}_v1.md"
    payload = build_customer_report_payload(customer_name)

    html_path.write_text(build_customer_report_html(customer_name))
    markdown_path.write_text(payload["markdown"])

    return {
        "status": "ok",
        "html_file": str(html_path),
        "markdown_file": str(markdown_path),
        "payload": payload,
    }
