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
# pyrefly: ignore [missing-import]
import plotly.express as px
import seaborn as sns
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Optional, Literal


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
                process_data=pddata.sample(10).to_html(classes="table table-striped custom-table")
            elif parameter=='statistics':
                process_data=dprofiling.analysis(pddata).to_html(classes="table table-striped custom-table")
            elif parameter=='description':
                info_df = pandas.DataFrame({
                    "Column": pddata.columns,
                    "Non-Null Count": pddata.notnull().sum().values,
                    "Data Type": pddata.dtypes.values
                })
                process_data=info_df.to_html(classes="table table-striped custom-table")
            elif parameter=='summary':
                process_data=pddata.describe().to_html(classes="table table-striped custom-table")
            else:
                process_data=pddata.sample(10).to_html(classes="table table-striped custom-table")
        except Exception as e:
            message = f"Error reading file"

    return templates.TemplateResponse(
        request=request, 
        name="data-profiling.html",
        context={
            "project_file":project_file,
            "parameter":parameter,
            "data": data,
            "columns": columns,
            "pdf": process_data
            }
        )


@app.get("/univariate-analysis", response_class=HTMLResponse, name="univariate-analysis")
async def univariateanalysis(request: Request):
    project_file = json.load(open("metadata/assign-project.json"))

    query_params = request.query_params
    field_name=query_params.get("field_name")
    plot_type=query_params.get("plot_type")

    graph_html=None
    if project_file:
        source_file=os.path.join('uploads',project_file[0]['file_name'])
        try:
            pddata=pandas.read_csv(source_file, header=0)
            if plot_type == 'histogram':
                fig = px.histogram(pddata, x=field_name, title="Histogram")
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'boxplot':
                fig = px.box(pddata,y=field_name, title="Boxplot")
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'violin':
                fig = px.violin(pddata,y=field_name, title="Violin Plot")
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'strip':
                fig = px.strip(pddata,y=field_name, title="Strip Plot")
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'ecdf':
                fig = px.strip(pddata,x=field_name, title="ECDF (Empirical Cumulative Distribution)")
                graph_html = fig.to_html(full_html=False)
            
            elif plot_type == 'bar':
                fig = px.bar(pddata[field_name].value_counts().reset_index(), x=field_name, y="count", title="Bar Chart")
                graph_html = fig.to_html(full_html=False)    
            elif plot_type == 'pie':
                fig = px.pie(pddata, names=field_name, title="Pie Chart")
                graph_html = fig.to_html(full_html=False) 
            elif plot_type == 'funnel':
                fig = px.bar(pddata[field_name].value_counts().reset_index(), x="count", y=field_name, title="Funnel Chart")
                graph_html = fig.to_html(full_html=False) 
            else: 
                fig = px.histogram(pddata, x=field_name, title="Histogram-others")
                graph_html = fig.to_html(full_html=False)

        except Exception as e:
            message = f"Error reading file"

    return templates.TemplateResponse(
        request=request, 
        name="univariate-analysis.html",
        context={
            "column": pddata.columns,
            "plot_type": plot_type,
            "field_name": field_name,
            "graph": graph_html
            }
        )

@app.get("/bivariate-analysis", response_class=HTMLResponse, name="bivariate-analysis")
async def bivariateanalysis(request: Request):
    project_file = json.load(open("metadata/assign-project.json"))

    query_params = request.query_params
    field_name_x=query_params.get("field_name_x")
    field_name_y=query_params.get("field_name_y")
    plot_type=query_params.get("plot_type")

    graph_html=None
    if project_file:
        source_file=os.path.join('uploads',project_file[0]['file_name'])
        try:
            pddata=pandas.read_csv(source_file, header=0)
            if plot_type == 'scatter':
                fig = px.scatter(pddata, x=field_name_x, y=field_name_y, title='Scatter Plot')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'line':
                fig = px.line(pddata, x=field_name_x, y=field_name_y, title='Line Plot')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'density_heatmap':
                fig = px.density_heatmap(pddata, x=field_name_x, y=field_name_y, title='Density Heatpmap')
                graph_html = fig.to_html(full_html=False) 
            elif plot_type == 'trendline':   #kaj kore na
                fig = px.scatter(pddata, x=field_name_x, y=field_name_y, trendline="ols", title='Scatter with Trendline')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'bar':
                 fig = px.bar(pddata, x=field_name_x, y=field_name_y, title='Bar Chart')
                 graph_html = fig.to_html(full_html=False) 
            elif plot_type == 'violin':
                fig = px.violin(pddata, x=field_name_x, y=field_name_y, title='Violin Plot')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'box':
                fig = px.box(pddata, x=field_name_x, y=field_name_y, title='Box Plot')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'strip':   #kaj kore na 
                fig = px.Strip(pddata, x=field_name_x, y=field_name_y, title='Strip Plot')
                graph_html = fig.to_html(full_html=False)

            elif plot_type == 'crosstab': #kaj kore na
                ct = pddata.crosstab(pddata[field_name_x], pddata[field_name_y])
                fig = px.imshow(ct, text_auto=True)
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'histogram':
                fig = px.histogram(pddata, x=field_name_x, color=field_name_y, barmode="group", title='Grouped Bar Chart')
                graph_html = fig.to_html(full_html=False)
            elif plot_type == 'sunburst':
                fig = px.sunburst(pddata, path=[field_name_x,field_name_y], title='Sunburst Chart')
                graph_html = fig.to_html(full_html=False)
            else: 
                graph_html = None

        except Exception as e:
            message = f"Error reading file"

    return templates.TemplateResponse(
        request=request, 
        name="bivariate-analysis.html",
        context={
            "column": pddata.columns,
            "plot_type": plot_type,
            "field_name_x": field_name_x,
            "field_name_y": field_name_y,
            
            "graph": graph_html
            }
        )


@app.get("/multivariate-analysis", response_class=HTMLResponse, name="multivariate-analysis")
async def multivariateanalysis(request: Request):
    project_file = json.load(open("metadata/assign-project.json"))
    query_params = list(request.query_params.keys())
    graph_html=None
    if project_file:
        source_file=os.path.join('uploads',project_file[0]['file_name'])
        pddatax=pandas.read_csv(source_file, header=0)
        try:
            if query_params:
                pddata=pandas.read_csv(source_file, header=0,usecols=query_params)
            else:
                pddata=pandas.read_csv(source_file, header=0)
            numeric_df = pddata.select_dtypes(include=[np.number])
             # Correlation Matrix
            corr = numeric_df.corr()
            n_cols = len(corr) 
            # Plotly Heatmap
            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale='RdBu_r'
            )
            fig.update_layout(
            width=1100,
            height= 900,
            margin=dict(
                l=0,
                r=0,
                t=20,
                b=0
            ))
            # Convert Figure to HTML
            graph_html = fig.to_html(full_html=False,config={"responsive": True})

        except Exception as e:
            message = f"Error reading file"
    return templates.TemplateResponse(
        request=request, 
        name="multivariate-analysis.html",
        context={
            "column": pddatax.columns,
            "correlation": corr.to_html(classes="table table-striped custom-table"),
            "graph": graph_html,
            'query_params':query_params
            }
        )


@app.get("/outlier-detection", response_class=HTMLResponse, name="outlier-detection")
async def outierdetection(request: Request):
    project_file = json.load(open("metadata/assign-project.json"))
    query_params = request.query_params
    
    OutlierResult=None

    if project_file:
        source_file=os.path.join('uploads',project_file[0]['file_name'])
        try:
            pddata=pandas.read_csv(source_file, header=0)
            numeric_df = pddata.select_dtypes(include=[np.number])
            
            #series = numeric_df[query_params.get('field_name')]
            series = numeric_df[field_name].dropna().reset_index(drop=True)
            outlier_mask = pd.Series([False] * len(series))
 
            if query_params.get('method_name') == "zscore":
                threshold = query_params.get('threshold') or 3.0
                z_scores = np.abs(stats.zscore(series))
                outlier_mask = z_scores > threshold
         
            elif query_params.get('method_name') == "iqr":
                threshold = query_params.get('threshold') or 1.5
                Q1 = series.quantile(0.25)
                Q3 = series.quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
                outlier_mask = (series < lower) | (series > upper)
         
            elif query_params.get('method_name') == "modified_zscore":
                threshold = query_params.get('threshold') or 3.5
                median = series.median()
                mad = np.median(np.abs(series - median))
                modified_z = 0.6745 * (series - median) / (mad if mad != 0 else 1e-10)
                outlier_mask = np.abs(modified_z) > threshold
           
            outlier_indices = list(numeric_df[outlier_mask].index.astype(int))
            outlier_values = list(series[outlier_mask])
            inlier_values = list(series[~outlier_mask])

            OutlierResult={
                "total_points": len(series),
                "outlier_count": int(outlier_mask.sum()),
                "outlier_indices": outlier_indices,
                "outlier_values": outlier_values,
                "inlier_values": inlier_values,
                "method": query_params.get('method_name'),
                "threshold_used": query_params.get('threshold'),
                "stats": {
                    "mean": round(float(series.mean()), 4),
                    "std": round(float(series.std()), 4),
                    "median": round(float(series.median()), 4),
                    "min": round(float(series.min()), 4),
                    "max": round(float(series.max()), 4),
                    "q1": round(float(series.quantile(0.25)), 4),
                    "q3": round(float(series.quantile(0.75)), 4),
                }
            }

        except Exception as e:
            message = f"Error reading file"
    
    return templates.TemplateResponse(
        request=request,
        name="outlier-detection.html",
        context={
            "column": pddata.columns,
            "OutlierResult": outlier_mask.tolist()
        })

@app.get("/visualization", response_class=HTMLResponse, name="visualization")
async def visualization(request: Request, name: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"name":name})




