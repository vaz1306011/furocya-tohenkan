# api/routes/view.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from api.services.convert import WORK

router = APIRouter()


@router.get("/view/{uid}")
def view(uid: str):
    pdf_path = WORK / f"{uid}.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    headers = {"Content-Disposition": f'inline; filename="{uid}.pdf"'}
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        headers=headers,
    )
