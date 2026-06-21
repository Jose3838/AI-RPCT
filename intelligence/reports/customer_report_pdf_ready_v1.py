from pathlib import Path
from datetime import datetime, timezone

SOURCE = Path("data/reports/customer_report_v1.md")
TARGET = Path("data/reports/customer_report_pdf_ready_v1.md")


def customer_report_pdf_ready_v1():
    if not SOURCE.exists():
        return {
            "status": "missing_source",
            "source": str(SOURCE)
        }

    content = SOURCE.read_text()

    pdf_ready = f"""# AI-RPCT Customer Intelligence Report

Generated: {datetime.now(timezone.utc).isoformat()}

---

{content}

---

Prepared by AI-RPCT
GPU Cloud Intelligence Terminal
"""

    TARGET.write_text(pdf_ready)

    return {
        "status": "saved",
        "file": str(TARGET),
        "chars": len(pdf_ready)
    }
