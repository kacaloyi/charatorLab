from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from router.auth import check_token,pwd_context
from controls.control import ControlRoom,ControlUser
from controls.controlChat import ControlChat

from pydantic import ValidationError

from sqlalchemy.orm import Session
from models.db import *
from models.schemas import *
#from models.models  import *
from conf.config import *
from utils.auth import *

from router.pages import templates


router = APIRouter()



# 聊天，发送消息
@router.post("/api/chat", response_model=None)
async def chat(request: Request,chat_data:dict ,  current_user:User=Depends(check_token)):
    try:
        
        chatdata =  dChartUser(**chat_data) 
       
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}
        
    chat =  ControlChat()   
    room ,message ,img = chat.Chat(chatdata, current_user)
    human_tps = templates.get_template("chathuman.html")
    bot_tps   = templates.get_template("chatbot.html")
    msg_human = human_tps.render({"request": request,"user": current_user,"content":chatdata.message})
    msg_bot   = bot_tps.render({"request": request,"room": room,"content":message,"img":img})

    generated =  msg_bot  + msg_human   

    return {'statu':'ok','info':generated} 

@router.post("/api/clear",response_model=None)
async def clear(request: Request,chat_data:dict ,  current_user:User=Depends(check_token)):
    try:
        
        chatdata =  dChartUser(**chat_data) 
       
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}
        
    chat =  ControlChat()  
    chat.clear(room_id = chat_data.room_id,user_id=current_user.id)

    return {'statu':'ok','info':"clear complateed"} 