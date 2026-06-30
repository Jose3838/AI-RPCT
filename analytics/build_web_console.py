from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WEB = ROOT / "web"
PAGES = WEB / "pages"
CSS = WEB / "assets" / "css" / "style.css"
JS = WEB / "assets" / "js" / "app.js"

DATA = ROOT / "data"

PAGES_CONFIG = [
    ("dashboard", "Dashboard", "Pipeline status, KPIs, and platform overview."),
    ("registry", "Registry Explorer", "Browse generated AI-RPCT registries."),
    ("infrastructure", "Infrastructure", "Providers, accelerators, and capacity data."),
    ("forecast", "Forecast Center", "Forecast dataset, engine output, and explanations."),
    ("analytics", "Analytics", "DuckDB analytics and SQL-generated summaries."),
    ("governance", "Governance", "Data quality, lineage, health, and release status."),
    ("api", "API Explorer", "FastAPI endpoints and query examples."),
    ("documentation", "Documentation", "Reports, architecture notes, and governance docs."),
]


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def html_escape(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def row_count(filename: str) -> int:
    return len(load_csv(DATA / filename))


def navigation(prefix: str = "") -> str:
    return "\n".join(
        f'<a href="{prefix}pages/{slug}.html">{title}</a>'
        for slug, title, _ in PAGES_CONFIG
    )


def page_navigation() -> str:
    return "\n".join(
        f'<a href="{slug}.html">{title}</a>'
        for slug, title, _ in PAGES_CONFIG
    )


def render_table(rows: list[dict[str, str]], limit: int = 30) -> str:
    if not rows:
        return "<p>No data available.</p>"

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
<div class="table-wrap">
  <table>
    <thead><tr>{header}</tr></thead>
    <tbody>{body}</tbody>
  </table>
</div>
{more}
"""


def metric_card(label: str, value: str) -> str:
    return f"""
<div class="card">
  <strong>{html_escape(label)}</strong>
  <span>{html_escape(value)}</span>
</div>
"""


def page_shell(title: str, description: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html_escape(title)} · AI-RPCT</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand">AI-RPCT</div>
    <nav>
      <a href="../index.html">Home</a>
      {page_navigation()}
    </nav>
  </aside>

  <main class="content">
    <section class="hero">
      <p class="eyebrow">AI-RPCT Module</p>
      <h1>{html_escape(title)}</h1>
      <p>{html_escape(description)}</p>
    </section>

    {body}
  </main>

  <script src="../assets/js/app.js"></script>
</body>
</html>
"""


def write_index() -> None:
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI-RPCT Web Console</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand">AI-RPCT</div>
    <nav>
      {navigation()}
    </nav>
  </aside>

  <main class="content">
    <section class="hero">
      <p class="eyebrow">Governed AI Infrastructure Intelligence</p>
      <h1>AI-RPCT Web Console</h1>
      <p>
        Explore registries, infrastructure metadata, forecast outputs,
        analytics, governance, API endpoints, and platform documentation.
      </p>
    </section>

    <section class="grid">
      {metric_card("Pipeline", "SUCCESS")}
      {metric_card("Registries", str(row_count("registry_metadata.csv")))}
      {metric_card("Forecast Records", str(row_count("forecast_engine_v1_output.csv")))}
      {metric_card("API", "FastAPI v2")}
    </section>

    <section class="panel">
      <h2>Console Sections</h2>
      <div class="section-list">
        {navigation()}
      </div>
    </section>
  </main>

  <script src="assets/js/app.js"></script>
</body>
</html>
"""
    (WEB / "index.html").write_text(html, encoding="utf-8")


def write_dashboard_page() -> None:
    pipeline_health = load_csv(DATA / "pipeline_health_summary.csv")
    data_quality = load_csv(DATA / "data_quality_metrics.csv")
    forecast_summary = load_csv(DATA / "forecast_run_summary.csv")

    body = f"""
<section class="grid">
  {metric_card("Pipeline Status", "SUCCESS")}
  {metric_card("Registries", str(row_count("registry_metadata.csv")))}
  {metric_card("Providers", str(row_count("provider_entity_registry.csv")))}
  {metric_card("Accelerators", str(row_count("unified_accelerator_registry.csv")))}
  {metric_card("Feature Records", str(row_count("feature_store.csv")))}
  {metric_card("Forecast Records", str(row_count("forecast_engine_v1_output.csv")))}
  {metric_card("Data Quality Checks", str(row_count("data_quality_metrics.csv")))}
  {metric_card("ML Production Promotions", "0")}
</section>

<section class="panel">
  <h2>Pipeline Health</h2>
  {render_table(pipeline_health)}
</section>

<section class="panel">
  <h2>Data Quality</h2>
  {render_table(data_quality)}
</section>

<section class="panel">
  <h2>Forecast Run Summary</h2>
  {render_table(forecast_summary)}
</section>
"""
    (PAGES / "dashboard.html").write_text(
        page_shell(
            "Dashboard",
            "Pipeline status, KPIs, health checks, and platform overview.",
            body,
        ),
        encoding="utf-8",
    )


def write_registry_page() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Registry Explorer · AI-RPCT</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand">AI-RPCT</div>
    <nav>
      <a href="../index.html">Home</a>
      """ + page_navigation() + """
    </nav>
  </aside>

  <main class="content">
    <section class="hero">
      <p class="eyebrow">AI-RPCT Registry Layer</p>
      <h1>Registry Explorer</h1>
      <p id="registryStatus">Loading registries...</p>
    </section>

    <section class="panel">
      <h2>Registry List</h2>
      <div class="table-wrap">
        <table>
          <tbody id="registryRows">
            <tr><td>Loading...</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <script src="../assets/js/api.js"></script>
  <script src="../assets/js/ui.js"></script>
  <script src="../assets/js/platform.js"></script>
  <script src="../assets/js/registry.js"></script>
</body>
</html>
"""
    (PAGES / "registry.html").write_text(html, encoding="utf-8")

def write_infrastructure_page() -> None:
    providers = load_csv(DATA / "provider_entity_registry.csv")
    relationships = load_csv(DATA / "provider_relationship_registry.csv")
    accelerators = load_csv(DATA / "unified_accelerator_registry.csv")
    capacity = load_csv(DATA / "historical_capacity_registry.csv")

    body = f"""
<section class="grid">
  {metric_card("Providers", str(len(providers)))}
  {metric_card("Provider Relationships", str(len(relationships)))}
  {metric_card("Accelerators", str(len(accelerators)))}
  {metric_card("Capacity Records", str(len(capacity)))}
</section>

<section class="panel">
  <h2>Provider Entities</h2>
  {render_table(providers, limit=20)}
</section>

<section class="panel">
  <h2>Provider Relationships</h2>
  {render_table(relationships, limit=20)}
</section>

<section class="panel">
  <h2>Unified Accelerators</h2>
  {render_table(accelerators, limit=20)}
</section>

<section class="panel">
  <h2>Historical Capacity</h2>
  {render_table(capacity, limit=20)}
</section>
"""
    (PAGES / "infrastructure.html").write_text(
        page_shell(
            "Infrastructure",
            "Providers, accelerator inventory, relationships, and capacity observations.",
            body,
        ),
        encoding="utf-8",
    )

def write_default_page(slug: str, title: str, description: str) -> None:
    body = """
<section class="panel">
  <h2>Status</h2>
  <p>This page is part of the AI-RPCT Web Console framework.</p>
  <p>Detailed data views will be wired into this module in the next sprint.</p>
</section>
"""
    (PAGES / f"{slug}.html").write_text(
        page_shell(title, description, body),
        encoding="utf-8",
    )


def write_assets() -> None:
    """
    Legacy no-op.

    CSS and JavaScript assets are maintained manually under:
    - web/assets/css/
    - web/assets/js/

    The web console generator must only generate HTML pages.
    Do not write style.css, app.js, or any JS/CSS asset here.
    """
    return


def main() -> None:
    # Assets are maintained manually. This generator only writes HTML pages.
    # write_assets()
    write_index()
    write_dashboard_page()
    write_registry_page()
    write_infrastructure_page()

    for slug, title, description in PAGES_CONFIG:
        if slug in {"dashboard", "registry", "infrastructure"}:
            continue

        write_default_page(slug, title, description)

    print("Web console generated.")
    print(WEB / "index.html")


if __name__ == "__main__":
    main()
