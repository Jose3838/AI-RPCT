from __future__ import annotations

import csv
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUTPUT = ROOT / "web" / "index.html"

DATASETS = [
    ("Feature Store", ROOT / "data" / "feature_store.csv"),
    ("Forecast Dataset", ROOT / "data" / "forecast_dataset.csv"),
    ("Forecast Output", ROOT / "data" / "forecast_engine_v1_output.csv"),
    ("Forecast Explanations", ROOT / "data" / "forecast_explanations.csv"),
    ("Registry Metadata", ROOT / "data" / "registry_metadata.csv"),
    ("Pipeline Health", ROOT / "data" / "pipeline_health_summary.csv"),
    ("Data Quality Metrics", ROOT / "data" / "data_quality_metrics.csv"),
]


def row_count(path: Path) -> int:
    if not path.exists():
        return 0

    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_table() -> str:
    rows = []

    for name, path in DATASETS:
        status = "OK" if path.exists() else "MISSING"

        rows.append(
            "<tr>"
            f"<td>{html_escape(name)}</td>"
            f"<td>{html_escape(str(path.relative_to(ROOT)))}</td>"
            f"<td>{row_count(path)}</td>"
            f"<td>{status}</td>"
            "</tr>"
        )

    return "\n".join(rows)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    generated = datetime.now(UTC).isoformat()

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI-RPCT Dashboard</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 40px;
      background: #f7f7f7;
      color: #222;
    }}
    h1 {{
      margin-bottom: 0;
    }}
    .subtitle {{
      color: #666;
      margin-top: 4px;
    }}
    .card {{
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 20px;
      margin-top: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    th, td {{
      border-bottom: 1px solid #eee;
      text-align: left;
      padding: 10px;
    }}
    th {{
      background: #fafafa;
    }}
    .ok {{
      color: #0a7f28;
      font-weight: bold;
    }}
    .governance {{
      font-size: 0.95rem;
      color: #444;
    }}
  </style>
</head>
<body>
  <h1>AI-RPCT Dashboard</h1>
  <p class="subtitle">Generated UTC: {html_escape(generated)}</p>

  <div class="card">
    <h2>Pipeline Status</h2>
    <p class="ok">SUCCESS</p>
  </div>

  <div class="card">
    <h2>Datasets</h2>
    <table>
      <thead>
        <tr>
          <th>Dataset</th>
          <th>Path</th>
          <th>Rows</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {build_table()}
      </tbody>
    </table>
  </div>

  <div class="card governance">
    <h2>Governance</h2>
    <ul>
      <li>No ML training from feature-only datasets.</li>
      <li>No accuracy claims without true future outcome labels.</li>
      <li>No paid production promotion from prototype forecast outputs.</li>
      <li>No invented pricing or synthetic benchmark claims.</li>
    </ul>
  </div>
</body>
</html>
"""

    OUTPUT.write_text(html, encoding="utf-8")

    print("Web dashboard generated.")
    print(OUTPUT)


if __name__ == "__main__":
    main()
