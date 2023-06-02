
import os
import random
import uvicorn
from typing import List,Dict,Any
import dotenv#加载.env中的设定值
dotenv.load_dotenv()


from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.staticfiles import StaticFiles


from utils.exception import request_validation_exception_handler,register_middleware,register_exception
from router.auth import UnAuthorizedException



from fastapi.middleware.cors import CORSMiddleware
from router import pages,auth,upload,api,chat,pay ,vector
#from db import SessionLocal, engine

#Python FastAPI 框架 操作Mysql数据库 增删改查
#https://blog.csdn.net/weixin_46703850/article/details/128732274

# pip install sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple

#uvicorn main:app --reload
#INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

#另一种启动方法 
#python main.py
#让 __name__ == '__main__'起作用

# 1、创建数据库表
#models.Base.metadata.create_all(bind=engine)
#from admin import app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 可选，用于模板引擎渲染网页
app.mount("/static", StaticFiles(directory="static"), name="static")

#统一处理异常
@app.exception_handler(UnAuthorizedException)
def exception_callback(request: Request, exc: Exception):
    return RedirectResponse("/user/login")


#加载路由
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(api.router)
app.include_router(pages.router)
app.include_router(chat.router)
app.include_router(pay.router)
app.include_router(vector.router)






        

    






    










if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000,reload=True)