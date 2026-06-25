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
    rows = load_csv(DATA / "registry_metadata.csv")

    body = f"""
<section class="grid">
  {metric_card("Registry Metadata", f"{len(rows)} rows")}
  {metric_card("Source", "data/registry_metadata.csv")}
  {metric_card("Status", "Active")}
  {metric_card("Mode", "Generated")}
</section>

<section class="panel">
  <h2>Registry Metadata Table</h2>
  {render_table(rows, limit=60)}
</section>
"""
    (PAGES / "registry.html").write_text(
        page_shell(
            "Registry Explorer",
            "Browse generated AI-RPCT registries, row counts, warehouse groups, and status.",
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
    CSS.write_text(
        """
:root {
  --bg: #07111f;
  --panel: #0f1c2e;
  --text: #eef5ff;
  --muted: #9fb2cc;
  --accent: #46e0a8;
  --border: rgba(255,255,255,0.12);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}

.sidebar {
  border-right: 1px solid var(--border);
  background: #081427;
  padding: 28px 20px;
}

.brand {
  font-size: 24px;
  font-weight: 900;
  margin-bottom: 28px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

nav a,
.section-list a {
  color: var(--muted);
  text-decoration: none;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid transparent;
}

nav a:hover,
.section-list a:hover {
  color: var(--text);
  border-color: var(--border);
}

.content {
  padding: 38px;
  overflow-x: hidden;
}

.hero {
  background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.035));
  border: 1px solid var(--border);
  border-radius: 26px;
  padding: 38px;
  margin-bottom: 24px;
}

.eyebrow {
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 13px;
  font-weight: 800;
}

h1 {
  font-size: 48px;
  margin: 10px 0 16px;
}

p {
  color: var(--muted);
  line-height: 1.6;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.card,
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 22px;
  margin-bottom: 24px;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card span {
  color: var(--accent);
  font-weight: 800;
  word-break: break-word;
}

.section-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.table-wrap {
  width: 100%;
  overflow-x: auto;
  margin-top: 16px;
}

table {
  width: 100%;
  min-width: 760px;
  border-collapse: collapse;
}

th,
td {
  border-bottom: 1px solid var(--border);
  padding: 11px 10px;
  text-align: left;
  vertical-align: top;
  font-size: 14px;
}

th {
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .7px;
  font-size: 12px;
}

.muted {
  color: var(--muted);
}

@media (max-width: 900px) {
  body {
    grid-template-columns: 1fr;
  }

  .grid,
  .section-list {
    grid-template-columns: 1fr;
  }
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    JS.write_text(
        'console.log("AI-RPCT Web Console loaded");\n',
        encoding="utf-8",
    )


def main() -> None:
    WEB.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    CSS.parent.mkdir(parents=True, exist_ok=True)
    JS.parent.mkdir(parents=True, exist_ok=True)

    write_assets()
    write_index()
    write_dashboard_page()
    write_registry_page()

    for slug, title, description in PAGES_CONFIG:
        if slug in {"dashboard", "registry"}:
            continue

        write_default_page(slug, title, description)

    print("Web console generated.")
    print(WEB / "index.html")


if __name__ == "__main__":
    main()
