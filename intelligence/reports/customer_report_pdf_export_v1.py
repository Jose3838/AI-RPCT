from pathlib import Path
from datetime import datetime, timezone

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

SOURCE = Path("data/reports/customer_report_pdf_ready_v1.md")
TARGET = Path("data/reports/customer_report_v1.pdf")


def customer_report_pdf_export_v1():
    if not SOURCE.exists():
        return {
            "status": "missing_source",
            "source": str(SOURCE)
        }

    text = SOURCE.read_text()

    TARGET.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(TARGET), pagesize=letter)
    width, height = letter

    x = inch
    y = height - inch
    line_height = 14

    c.setFont("Helvetica", 10)

    for raw_line in text.splitlines():
        line = raw_line[:95]

        if y < inch:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - inch

        c.drawString(x, y, line)
        y -= line_height

    c.save()

    return {
        "status": "saved",
        "file": str(TARGET),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
