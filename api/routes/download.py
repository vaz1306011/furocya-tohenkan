# api/routes/download.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from api.services.convert import WORK

router = APIRouter()


@router.get("/download/{uid}")
def download(uid: str):
    pdf_path = WORK / f"{uid}.pdf"
    name_path = WORK / f"{uid}.name"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if name_path.exists():
        filename = f"{name_path.read_text(encoding='utf-8').strip()}.pdf"
    else:
        filename = f"{uid}.pdf"
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename,
    )
