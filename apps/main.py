# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Optional, List

app = FastAPI(Debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
templates.env.cache_size = 0  # cache error fix

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})

@app.get("/dataupload", response_class=HTMLResponse, name="dataupload")
async def dataupload(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="data-upload.html",context={"name":name})


@app.get("/dataprofiling", response_class=HTMLResponse, name="dataprofiling")
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




