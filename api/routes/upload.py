# api/routes/upload.py
import logging

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse

from api.services.convert import convert_c_to_pdf

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".c"):
        raise HTTPException(status_code=400, detail="Only .c files are supported")
    try:
        uid = await convert_c_to_pdf(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Conversion failed")
        raise HTTPException(status_code=500, detail="Conversion failed") from exc
    view_url = f"/view/{uid}"
    download_url = f"/download/{uid}"
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return {"view": view_url, "download": download_url}
    return RedirectResponse(download_url, status_code=303)
