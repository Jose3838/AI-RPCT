from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import FileResponse

from security.api_keys import validate_api_key

router = APIRouter()

@router.get("/download/customer-report")
def download_customer_report(x_api_key: str | None = Header(None)):
    if not x_api_key or not validate_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")

    path = "data/reports/customer_report_v1.pdf"
    try:
        return FileResponse(path, media_type="application/pdf", filename="AI-RPCT-Customer-Intelligence-Report.pdf")
    except Exception:
        return {"status": "missing_file", "path": path}
