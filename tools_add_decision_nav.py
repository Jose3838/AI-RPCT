from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
PAGES = WEB / "pages"

DECISION_LINK_INDEX = '<a href="pages/decision.html">Decision Center</a>'
DECISION_LINK_PAGE = '<a href="decision.html">Decision Center</a>'


def ensure_decision_page():
    path = PAGES / "decision.html"
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI-RPCT Decision Center</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <h1>AI-RPCT Decision Center</h1>

    <section class="card">
        <h2>Latest Recommendation</h2>
        <div id="decision-card">Loading latest recommendation...</div>
    </section>

    <script src="../app.js"></script>
</body>
</html>
""",
        encoding="utf-8",
    )


def add_link(path: Path, link: str):
    text = path.read_text(encoding="utf-8")

    if "Decision Center" in text:
        return

    marker = "</nav>"

    if marker in text:
        text = text.replace(marker, f"      {link}\n    {marker}")
    else:
        text = text.replace("</body>", f"{link}\n</body>")

    path.write_text(text, encoding="utf-8")


def main():
    ensure_decision_page()

    index = WEB / "index.html"
    if index.exists():
        add_link(index, DECISION_LINK_INDEX)

    for page in PAGES.glob("*.html"):
        add_link(page, DECISION_LINK_PAGE)

    print("Decision Center page and navigation updated.")


if __name__ == "__main__":
    main()
