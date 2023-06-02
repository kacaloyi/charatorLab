
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response

from router.auth import check_token,pwd_context
from controls.control import ControlRoom,ControlUser
from models.schemas import *
from models.db import *
#from models.models  import *

# 实例化Jinja2Templates类
templates = Jinja2Templates(directory="views")


router = APIRouter()







@router.get("/uc/vip", response_class=HTMLResponse)
async def ucvip(request: Request): 
    return templates.TemplateResponse("usercentervip.html",{"request": request,"urls":"你要什么？"})

@router.get("/uc/say", response_class=HTMLResponse)#投诉、建议
async def ucsay(request: Request): 
    return templates.TemplateResponse("usercentersay.html",{"request": request,"urls":"你要什么？"})

@router.get("/uc/pay", response_class=HTMLResponse)#充值
async def ucpay(request: Request): 
    return templates.TemplateResponse("usercenterpay.html",{"request": request,"urls":"你要什么？"})

@router.get("/uc/qa", response_class=HTMLResponse)#常见问题，问答
async def ucqa(request: Request): 
    return templates.TemplateResponse("usercenterqa.html",{"request": request,"urls":"你要什么？"})

@router.get("/uc/share", response_class=HTMLResponse)#分享海报
async def ucshare(request: Request): 
    return templates.TemplateResponse("usercentershara.html",{"request": request,"urls":"你要什么？"})




#https://toutiao.io/posts/pkeimbu/preview  fastAPI和Flask的各种功能实现的比较。
#FastAPI 根据要求和需要，提供了相当多的响应类型。如果需要返回文件，可以用 FileResponse 或 StreamingResponse。
#这里还缺少文件型回复，就是下载文件或者播放流媒体。
@router.get("/", response_class=HTMLResponse)
async def index(request: Request): 
    rooms = ControlRoom.get_rooms()
    return templates.TemplateResponse("index.html",{"request": request,"rooms":rooms})

@router.get("/user/regist", response_class=HTMLResponse)
async def regist(request: Request): 
    return templates.TemplateResponse("regist.html",{"request": request,"urls":"你要什么？"})

#@app.post("/user/login", response_class=HTMLResponse)
@router.get("/user/login", response_class=HTMLResponse)
async def login(request: Request): 
    return templates.TemplateResponse("login.html",{"request": request,"urls":"你要什么？"})

@router.get("/roomlist", response_class=HTMLResponse)
async def roomlist(request: Request): 
    rooms = ControlRoom.get_rooms()
    return templates.TemplateResponse("roomlist.html",{"request": request,"rooms":rooms})

@router.get("/room/{roomid}", response_class=HTMLResponse)
async def room(roomid:int,request: Request,current_user:User=Depends(check_token)): 
    room = ControlRoom.get_room_by_id(roomid)
    if not room :
        RedirectResponse("/roomlist")

    return templates.TemplateResponse("room.html",{"request": request,"room":room,"user":current_user})

@router.get("/room/create/{roomid}", response_class=HTMLResponse)
async def roomcreate(request: Request,current_user:User=Depends(check_token)):    
    return templates.TemplateResponse("roomcreate.html",{"request": request,"user":current_user})


@router.get("/room/edit/{roomid}", response_class=HTMLResponse)
async def roomedit(roomid:int,request: Request,current_user:User=Depends(check_token)): 
    room = ControlRoom.get_room_by_id(roomid)
 
    print(room.categories+" "+room.public.value +" "+room.sound)
    disable = "disabled"
    if(room.owner_id==current_user.id ):
        disable = ""
      
    return templates.TemplateResponse("roomedit.html",{"request": request,"room":room,"user":current_user,"disable":disable})

@router.get("/uc", response_class=HTMLResponse)
async def usercenter(request: Request,current_user:User=Depends(check_token)): 

    return templates.TemplateResponse("usercenter.html",{"request": request,"user":current_user})

@router.get("/pay", response_class=HTMLResponse)
async def pay(request: Request,current_user:User=Depends(check_token)): 

    return templates.TemplateResponse("pay.html",{"request": request,"user":current_user})