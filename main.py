"""
main.py
---------------------------------------
FastAPI Server

Run:

uvicorn main:app --reload

Swagger:

http://127.0.0.1:8000/docs
"""

import io
import os
from unittest import result
import uuid
import traceback
import shutil
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from processor import processor
from config import TEMP_DIR

app = FastAPI(
    title="Image Processing Agent",
    version="2.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):

    try:

        ext = os.path.splitext(file.filename)[1]

        if ext == "":
            ext = ".jpg"

        temp_filename = f"{uuid.uuid4()}{ext}"

        temp_path = os.path.join(
            TEMP_DIR,
            temp_filename
        )

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = processor.process(temp_path)
        print("Image Mode:", result.mode)

        result.save("debug.png")
    
        os.remove(temp_path)

        buffer = io.BytesIO()

        result.save(
            buffer,
            format="PNG"
)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="image/png",
    
        )

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )