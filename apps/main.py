# main.py
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Optional, List
import shutil
import uuid
import os
from utils.json_handler import MetadataStore



app = FastAPI(Debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
#templates.env.cache_size = 0  # cache error fix

UPLOAD_DIR = Path("uploads")
store = MetadataStore()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    csv_data=store.get_all()
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"csv_data":csv_data})



@app.get("/dataupload", response_class=HTMLResponse, name="dataupload")
async def dataupload(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="data-upload.html",context={"name":name})


@app.post("/dataupload", response_class=HTMLResponse, name="dataupload")
async def dataupload_post(request: Request,csv_file: UploadFile = File(...)):
    
    form = await request.form()
    project_id=form.get("project_id")
    project_name=form.get("project_name")
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Validate file type
    if not csv_file.filename.endswith(".csv"):
        return templates.TemplateResponse(
            request=request, name="data-upload.html",
            context={
                "message": "Only CSV files are allowed!",
                "message_type": "error"
            }
        )

    # Generate unique filename to avoid overwrite
    unique_filename = f"{project_id}_{csv_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(csv_file.file, buffer)
        message = f"{csv_file.filename} uploaded and saved successfully!"

        store.add({
            "project_id": project_id,
            "project_name": project_name,
            "file_name": unique_filename,
            "mime_type": csv_file.content_type,
            "file_size": os.path.getsize(file_path)
        })

    except Exception as e:
        message = f"Error saving file: {str(e)}"

    finally:
        await csv_file.close()

    return templates.TemplateResponse(
        request=request, name="data-upload.html",
            context={
                "message": message,
                "message_type": "success"
            }
    )



@app.get("/data-profiling", response_class=HTMLResponse, name="data-profiling")
async def dataprofiling(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})


@app.get("/univariate-analysis", response_class=HTMLResponse, name="univariate-analysis")
async def univariateanalysis(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/bivariate-analysis", response_class=HTMLResponse, name="bivariate-analysis")
async def bivariateanalysis(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})


@app.get("/multivariate-analysis", response_class=HTMLResponse, name="multivariate-analysis")
async def multivariateanalysis(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})


@app.get("/outier-detection", response_class=HTMLResponse, name="outier-detection")
async def outierdetection(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/visualization", response_class=HTMLResponse, name="visualization")
async def visualization(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})




