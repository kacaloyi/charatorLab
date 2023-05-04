import os

from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response

from werkzeug.utils import secure_filename
from models.schemas import *  
from conf.config import *
from controls.control import *
from utils.auth import *

from fastapi import APIRouter


router = APIRouter()




ALLOWED_EXTENSIONS = {'txt','jpg','png'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file and allowed_file(file.filename):
        # 这个函数来自werkzeug.utils模块，用于安全处理文件名。它将文件名中的特殊字符替换为下划线，
        # 并删除文件名中的路径信息，以防止路径遍历攻击。
        filename = secure_filename(file.filename)
        bytes = await file.read()
        pathname = os.path.join(UPLOAD_FOLDER, filename)
        hostname = os.path.join(HOST_FOLDER,filename)
        with open(pathname, 'wb') as  f:
            f.write(bytes)# imgbytes includes the file format information, so fout.mrite(ingbytes) will save the bytes as image,video or others# fout.write(imgbase64) # if fout.write(imgbase64), the saved file is messy codefout.close()
            f.close()

        
        return {"hostname":hostname}
        """file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"filename": filename}"""
    file.close()
    return {"error": "file not allowed"}