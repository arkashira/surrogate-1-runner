from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uuid
import shutil
import os
import json

from .services.db import SessionLocal, Base, engine
from .services.parser import parse_tf, parse_yaml, parse_log
from .services.generator import generate_markdown, generate_html

app = FastAPI(title="Compliance Documentation Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Create DB tables
Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------- Routes ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    file_ids = []
    for f in files:
        ext = Path(f.filename).suffix.lower()
        if ext not in {".tf", ".yaml", ".yml", ".json", ".log", ".txt"}:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        file_id = str(uuid.uuid4())
        dest = UPLOAD_DIR / f"{file_id}{ext}"
        with dest.open("wb") as buffer:
            shutil.copyfileobj(f.file, buffer)

        file_ids.append({"id": file_id, "name": f.filename, "ext": ext})

        # Kick off background parsing
        background_tasks.add_task(process_file, file_id, dest, ext)

    return JSONResponse({"status": "queued", "files": file_ids})

@app.get("/docs/{file_id}", response_class=HTMLResponse)
async def get_doc(request: Request, file_id: str):
    # Fetch from DB
    from .services.db import get_file_record
    record = get_file_record(file_id)
    if not record:
        raise HTTPException(status_code=404, detail="Document not found")

    return templates.TemplateResponse("docs.html", {"request": request, "doc": record})

@app.get("/download/{file_id}")
async def download_doc(file_id: str):
    from .services.db import get_file_record
    record = get_file_record(file_id)
    if not record:
        raise HTTPException(status_code=404, detail="Document not found")

    return FileResponse(record.file_path, media_type="application/octet-stream", filename=f"{record.original_name}.html")

# ---------- Background Tasks ----------

def process_file(file_id: str, path: Path, ext: str):
    """Parse the file and generate docs."""
    try:
        if ext == ".tf":
            data = parse_tf(path)
        elif ext in {".yaml", ".yml"}:
            data = parse_yaml(path)
        elif ext in {".log", ".json", ".txt"}:
            data = parse_log(path)
        else:
            data = {"error": "Unsupported format"}

        md = generate_markdown(data)
        html = generate_html(md)

        # Store in DB
        from .services.db import store_file_record
        store_file_record(file_id, path.name, str(path), md, html)

    except Exception as e:
        # Log and store error
        from .services.db import store_file_error
        store_file_error(file_id, str(e))