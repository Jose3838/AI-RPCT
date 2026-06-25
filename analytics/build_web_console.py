from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WEB = ROOT / "web"
PAGES = WEB / "pages"
CSS = WEB / "assets" / "css" / "style.css"
JS = WEB / "assets" / "js" / "app.js"


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


def navigation() -> str:
    links = [
        f'<a href="pages/{slug}.html">{title}</a>'
        for slug, title, _ in PAGES_CONFIG
    ]

    return "\n".join(links)


def page_navigation() -> str:
    links = [
        f'<a href="{slug}.html">{title}</a>'
        for slug, title, _ in PAGES_CONFIG
    ]

    return "\n".join(links)


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
      <div class="card"><strong>Pipeline</strong><span>SUCCESS</span></div>
      <div class="card"><strong>Registries</strong><span>Auto Catalog</span></div>
      <div class="card"><strong>Forecast</strong><span>Rule-based v1</span></div>
      <div class="card"><strong>API</strong><span>FastAPI v2</span></div>
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


def write_page(slug: str, title: str, description: str) -> None:
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} · AI-RPCT</title>
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
      <h1>{title}</h1>
      <p>{description}</p>
    </section>

    <section class="panel">
      <h2>Status</h2>
      <p>This page is part of the AI-RPCT Web Console framework.</p>
      <p>Detailed data views will be wired into this module in the next sprint.</p>
    </section>
  </main>

  <script src="../assets/js/app.js"></script>
</body>
</html>
"""
    (PAGES / f"{slug}.html").write_text(html, encoding="utf-8")


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
}

.card {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card span {
  color: var(--accent);
  font-weight: 800;
}

.section-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

@media (max-width: 900px) {
  body {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
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

    for slug, title, description in PAGES_CONFIG:
        write_page(slug, title, description)

    print("Web console generated.")
    print(WEB / "index.html")


if __name__ == "__main__":
    main()
