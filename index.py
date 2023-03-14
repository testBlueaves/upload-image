import shutil
from typing import Union
import os
import aiofiles
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/output", StaticFiles(directory="output"), name="output")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "form_1": "select", "form_2": "deselect",
                                                     "success": "", "danger": ""})


@app.post("/upload")
def upload(request: Request, save: UploadFile = File(...)):
    if save.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']:
        return templates.TemplateResponse("index.html", {"danger": "alert-danger", "form_1": "select", "success": "",
                                                         "request": request})
    try:
        contents = save.file.read()
        with open('./output/img/' + save.filename, "wb") as f:
            f.write(contents)
    except FileNotFoundError:
        return {"message": "There was an error uploading the file"}
    finally:
        save.file.close()
    print(save.filename)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "danger": "",
                                       "image_name": save.filename, "success": "alert-success", "form_1": None})


@app.post("/addText")
def text(request: Request,text_kush: str = Form(), img_name: str = Form()):
    print(text_kush, img_name)
    try:
        with open('./output/word/' + text_kush + '.txt', "w", encoding='UTF-8') as file:
            file.write(text_kush)
        try:
            os.rename('output/img/' + img_name, 'output/img/' + text_kush + '.png')
        except:
            return {"eoor":"ha"}
    except FileNotFoundError:
        return {"message": "There was an error uploading the file"}
    print(text_kush, img_name)
    return templates.TemplateResponse("index.html",
                                      {"danger": "", "image_name": text_kush + '.png', "success": "alert-success",
                                       "form_1": None,"request": request})
