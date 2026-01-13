from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes import download, upload, view

app = FastAPI()
app.include_router(upload.router)
app.include_router(download.router)
app.include_router(view.router)

BASE_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = BASE_DIR / "web"
if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")
IMG_DIR = BASE_DIR / "img"
if IMG_DIR.exists():
    app.mount("/img", StaticFiles(directory=IMG_DIR), name="img")


@app.get("/")
def index():
    if not WEB_DIR.exists():
        return {"message": "web/index.html not found"}
    return FileResponse(WEB_DIR / "index.html")
