import os

from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response

from werkzeug.utils import secure_filename
from models.schemas import *  
from conf.config import *
from controls.control import *
from utils.auth import *
from PIL import Image

from fastapi import APIRouter


router = APIRouter()




ALLOWED_EXTENSIONS = {'txt','jpg','png'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if (file.size/1000 )> 500  :
        return {"error": "file is so big"}

    if file and allowed_file(file.filename):
        # 这个函数来自werkzeug.utils模块，用于安全处理文件名。它将文件名中的特殊字符替换为下划线，
        # 并删除文件名中的路径信息，以防止路径遍历攻击。
        filename = secure_filename(file.filename)
        pathname = os.path.join(UPLOAD_FOLDER, filename)
        hostname = os.path.join(HOST_FOLDER,filename)

        try: #如果image能打开，就是图片，改成正方形，并且改尺寸到256,保存。
           
           with Image.open(file) as image:
               # 裁剪成正方形
                width, height = image.size
                new_size = min(width, height)
                left = (width - new_size) / 2
                top = (height - new_size) / 2
                right = (width + new_size) / 2
                bottom = (height + new_size) / 2
                image = image.crop((left, top, right, bottom))
                # 缩放到指定大小
                image = image.resize((256, 256))
           
                image.save(pathname, 'JPEG')
        except:#不是图片，直接拷贝。
            bytes = await file.read()
            with open(pathname, 'wb') as  f:
                f.write(bytes)# imgbytes includes the file format information, so fout.mrite(ingbytes) will save the bytes as image,video or others# fout.write(imgbase64) # if fout.write(imgbase64), the saved file is messy codefout.close()
                f.close()

        
        return {"hostname":hostname}
        """file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"filename": filename}"""
    file.close()
    return {"error": "file not allowed"}