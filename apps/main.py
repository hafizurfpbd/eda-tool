# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional, List

app = FastAPI(Debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
templates.env.cache_size = 0  # cache error fix

@app.get("/")
async def home(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})
