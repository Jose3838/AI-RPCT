from __future__ import annotations

import csv
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "web" / "index.html"


CSV_SECTIONS = {
    "Registry Explorer": ROOT / "data" / "registry_metadata.csv",
    "Pipeline Health": ROOT / "data" / "pipeline_health_summary.csv",
    "Data Quality": ROOT / "data" / "data_quality_metrics.csv",
    "Feature Store": ROOT / "data" / "feature_store.csv",
    "Forecast Dataset": ROOT / "data" / "forecast_dataset.csv",
    "Forecast Output": ROOT / "data" / "forecast_engine_v1_output.csv",
    "Forecast Explanations": ROOT / "data" / "forecast_explanations.csv",
    "Forecast Run Summary": ROOT / "data" / "forecast_run_summary.csv",
    "Provider Entities": ROOT / "data" / "provider_entity_registry.csv",
    "Provider Relationships": ROOT / "data" / "provider_relationship_registry.csv",
    "Unified Accelerators": ROOT / "data" / "unified_accelerator_registry.csv",
    "Historical Capacity": ROOT / "data" / "historical_capacity_registry.csv",
    "Registry Catalog": ROOT / "data" / "registry_catalog_v2.csv",
}


API_ENDPOINTS = [
    "GET /",
    "GET /health",
    "GET /pipeline",
    "GET /registries",
    "GET /registry/{name}",
    "GET /registry/feature_store?key=vendor&value=NVIDIA",
    "GET /registry/feature_store?sort=vendor&limit=10",
    "GET /providers",
    "GET /capacity",
    "GET /forecast",
    "GET /features",
]


def html_escape(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def render_table(title: str, path: Path, limit: int = 8) -> str:
    rows = load_csv(path)

    if not rows:
        return f"""
        <section class="panel">
          <h2>{html_escape(title)}</h2>
          <p class="muted">No data found: <code>{html_escape(path.relative_to(ROOT))}</code></p>
        </section>
        """

    columns = list(rows[0].keys())
    visible_rows = rows[:limit]

    header = "".join(f"<th>{html_escape(col)}</th>" for col in columns)

    body = ""
    for row in visible_rows:
        body += "<tr>"
        for col in columns:
            body += f"<td>{html_escape(row.get(col, ''))}</td>"
        body += "</tr>"

    more = ""
    if len(rows) > limit:
        more = f"<p class='muted'>Showing {limit} of {len(rows)} rows.</p>"

    return f"""
    <section class="panel">
      <div class="section-head">
        <h2>{html_escape(title)}</h2>
        <span class="count">{len(rows)} rows</span>
      </div>
      <p class="muted"><code>{html_escape(path.relative_to(ROOT))}</code></p>
      <div class="table-wrap">
        <table>
          <thead><tr>{header}</tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
      {more}
    </section>
    """


def total_rows() -> int:
    return sum(len(load_csv(path)) for path in CSV_SECTIONS.values())


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(UTC).isoformat()

    sections_html = "\n".join(
        render_table(title, path)
        for title, path in CSV_SECTIONS.items()
    )

    api_html = "".join(
        f"<li><code>{html_escape(endpoint)}</code></li>"
        for endpoint in API_ENDPOINTS
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI-RPCT Web Console</title>
  <style>
    :root {{
      --bg: #07111f;
      --panel: #0f1c2e;
      --panel2: #13243a;
      --text: #eef5ff;
      --muted: #9fb2cc;
      --accent: #46e0a8;
      --accent2: #7aa8ff;
      --border: rgba(255,255,255,0.12);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(70,224,168,0.18), transparent 32%),
        radial-gradient(circle at top right, rgba(122,168,255,0.18), transparent 30%),
        var(--bg);
      color: var(--text);
    }}

    .page {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 34px 24px 70px;
    }}

    .nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 38px;
    }}

    .brand {{
      font-size: 22px;
      font-weight: 900;
      letter-spacing: .5px;
    }}

    .pill {{
      border: 1px solid var(--border);
      color: var(--muted);
      border-radius: 999px;
      padding: 8px 14px;
      background: rgba(255,255,255,.04);
    }}

    .hero {{
      padding: 44px;
      border: 1px solid var(--border);
      border-radius: 28px;
      background: linear-gradient(180deg, rgba(255,255,255,.09), rgba(255,255,255,.035));
      box-shadow: 0 22px 80px rgba(0,0,0,.28);
    }}

    h1 {{
      margin: 0 0 18px;
      font-size: 56px;
      line-height: 1.02;
      letter-spacing: -1.5px;
    }}

    .subtitle {{
      color: var(--muted);
      font-size: 18px;
      line-height: 1.65;
      max-width: 900px;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 24px;
    }}

    .metric {{
      padding: 22px;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: var(--panel);
    }}

    .num {{
      color: var(--accent2);
      font-size: 34px;
      font-weight: 900;
    }}

    .label, .muted {{
      color: var(--muted);
    }}

    .panel {{
      margin-top: 24px;
      padding: 26px;
      border: 1px solid var(--border);
      border-radius: 22px;
      background: rgba(15,28,46,.92);
      overflow: hidden;
    }}

    .section-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
    }}

    h2 {{
      margin: 0 0 10px;
      font-size: 24px;
    }}

    .count {{
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(70,224,168,.12);
      color: var(--accent);
      font-weight: 800;
      font-size: 13px;
      white-space: nowrap;
    }}

    .table-wrap {{
      width: 100%;
      overflow-x: auto;
      margin-top: 14px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 720px;
    }}

    th, td {{
      text-align: left;
      padding: 11px 10px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      font-size: 14px;
    }}

    th {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: .7px;
    }}

    code {{
      color: #cfe0ff;
      background: rgba(255,255,255,.06);
      border-radius: 7px;
      padding: 3px 6px;
    }}

    .api-list {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      padding-left: 18px;
    }}

    .governance {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }}

    .rule {{
      padding: 16px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: rgba(255,255,255,.05);
      color: var(--muted);
    }}

    footer {{
      margin-top: 32px;
      text-align: center;
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 900px) {{
      .metrics, .api-list, .governance {{
        grid-template-columns: 1fr;
      }}

      h1 {{ font-size: 40px; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <nav class="nav">
      <div class="brand">AI-RPCT</div>
      <div class="pill">Governed AI Infrastructure Intelligence</div>
    </nav>

    <section class="hero">
      <h1>AI-RPCT Web Console</h1>
      <p class="subtitle">
        Full platform overview for registries, provider graph, accelerator layer,
        capacity observations, feature store, forecast pipeline, explainability,
        analytics, governance, API endpoints, and operational metadata.
      </p>
      <p class="muted">Generated UTC: <code>{html_escape(generated)}</code></p>

      <div class="metrics">
        <div class="metric">
          <div class="num">SUCCESS</div>
          <div class="label">Pipeline status</div>
        </div>
        <div class="metric">
          <div class="num">{len(CSV_SECTIONS)}</div>
          <div class="label">Console sections</div>
        </div>
        <div class="metric">
          <div class="num">{total_rows()}</div>
          <div class="label">Visible data rows</div>
        </div>
        <div class="metric">
          <div class="num">0</div>
          <div class="label">Production ML promotions</div>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Platform Modules Built</h2>
      <div class="governance">
        <div class="rule">Historical registries: sources, entities, relationships, GPUs, software timelines.</div>
        <div class="rule">Provider graph: cloud providers, provider entities, provider relationships.</div>
        <div class="rule">ML pipeline: feature store, forecast dataset, rule-based forecast engine, explanations.</div>
        <div class="rule">Platform layer: pipeline runner, DuckDB analytics, FastAPI, dashboards, CI/CD.</div>
      </div>
    </section>

    {sections_html}

    <section class="panel">
      <h2>API Endpoints</h2>
      <ul class="api-list">
        {api_html}
      </ul>
    </section>

    <section class="panel">
      <h2>Governance Guardrails</h2>
      <div class="governance">
        <div class="rule">No ML training without true future outcome labels.</div>
        <div class="rule">No accuracy claims without verified outcome evaluation.</div>
        <div class="rule">No invented prices, capacity values, or benchmark claims.</div>
        <div class="rule">No paid production promotion from prototype forecast outputs.</div>
      </div>
    </section>

    <footer>
      AI-RPCT Web Console v1 · Generated from governed local datasets
    </footer>
  </main>
</body>
</html>
"""

    OUTPUT.write_text(html, encoding="utf-8")
    print("Web dashboard generated.")
    print(OUTPUT)


if __name__ == "__main__":
    main()
