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
import json
from utils.json_handler import MetadataStore
from utils.descriptive import Descriptive
import pandas
import statistics


app = FastAPI(Debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
#templates.env.cache_size = 0  # cache error fix

UPLOAD_DIR = Path("uploads")
store = MetadataStore()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/dashboard", response_class=HTMLResponse,name="dashboard")
async def dashboard(request: Request,project_id: Optional[str] = None):
    csv_data=store.get_all()

    status_message=None
    if project_id:
        assign_data=store.search('project_id',project_id)
        with open("metadata/assign-project.json", "w") as f: json.dump(assign_data, f, indent=2)
        status_message="Successfully project assigned"
    
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"csv_data":csv_data,"project_id":project_id,"status_message":status_message})



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
async def dataprofiling(request: Request, parameter: Optional[str] = None):
    
    project_file = json.load(open("metadata/assign-project.json"))
    data=None
    columns=None
    process_data=None
    dprofiling=Descriptive()

    if project_file:
        source_file=os.path.join('uploads',project_file[0]['file_name'])
        try:
            pddata=pandas.read_csv(source_file, header=0)
            if parameter=='sample-data':
                pddata_10=pddata.sample(10)
                data = pddata_10.to_dict('records')
                columns = pddata.columns.tolist()
            elif parameter=='statistics':
                process_data=dprofiling.analysis(pddata)
                data = process_data.to_dict('records')
                columns = process_data.columns.tolist()
            elif parameter=='missing-value':
                process_data=None
            elif parameter=='description':
                process_data=pddata.info()
                data = process_data.to_dict('records')
                columns = process_data.columns.tolist()
            elif parameter=='summary':
                process_data=pddata.describe()
                data = process_data.to_dict('records')
                columns = process_data.columns.tolist()
            else:
                pddata_10=pddata.sample(10)
                data = pddata_10.to_dict('records')
                columns = pddata.columns.tolist()
        except Exception as e:
            message = f"Error reading file"

    return templates.TemplateResponse(
        request=request, 
        name="data-profiling.html",
        context={
            "project_file":project_file,
            "data": data,
            "columns": columns,
            "pdf": process_data
            }
        )


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




