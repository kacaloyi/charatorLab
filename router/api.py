from fastapi.templating import Jinja2Templates
from fastapi import APIRouter,Request

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from router.auth import check_token,pwd_context
from controls.control import ControlRoom,ControlUser
from controls.controlChat import ControlChat

from pydantic import ValidationError

from sqlalchemy.orm import Session
from models.db import User,Room,Message,session,HistoryMoney,HistoryRoom,logTypeRoom
from models.db import *
from models.schemas import *
#from models.models  import *
from conf.config import *
from utils.auth import *


router = APIRouter()




# 4、创建您的FastAPI 路径操作
@router.get("/users/", response_model=List[dUser])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = ControlUser.get_users(skip=skip, limit=limit) 
    return users

# 4、创建您的FastAPI 路径操作
@router.get("/users/{user_id}", response_model=dUser)
def read_user(user_id: int, db:Session = Depends(get_db)):
    db_user =ControlUser.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


"""@app.get("/users/del/{userid}")#,response_model=schemas.User)
def del_user(userid:int,db:Session = Depends(get_db)):
    #print("user_id="+userid)
    user = crud.del_user(db,user_id=userid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return duser"""

# 4、创建您的FastAPI 路径操作
@router.post("/api/roomcreate", response_model=None)
def create_Room_for_user(room_data:dict, current_user:User=Depends(check_token)):#room: schemas.dRoomCreate
    try:
        # some code that raises a ValidationError
        room = dRoomCreate(**room_data)
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}

        
    newroom = ControlRoom.create_room(room,current_user)

    roommsg = HistoryRoom(wtype=logTypeRoom.roomcreate,user_id=current_user.id,room_id=newroom.id,info="创建")
    session.add(roommsg)
    session.commit()

    
    return  {"statu":"ok","room":newroom,"owner":current_user.id}


# 编辑room，不能编辑历史资料
@router.post("/api/roomedit", response_model=None)
def create_Room_for_user(room: dRoomEdit, current_user:User=Depends(check_token)):
    if(room.owner_id!=current_user.id):
      return {"statu":"ok","info":"别人的room不能改","owner":current_user.id}
    
    ControlRoom.edit_room(room=room,owner=current_user)
    ControlChat.clear(room_id= room.id,user_id=current_user.id)


    roommsg = HistoryRoom(wtype=logTypeRoom.roomedit,user_id=current_user.id,room_id=room.id,info="编辑")
    session.add(roommsg)
    session.commit()


    return {"statu":"ok","info":"ok","owner":current_user.id}

# 获取room表，可分页
@router.get("/api/roomlist/{skip}/{limit}", response_model=List[dRoom])
def read_Rooms(skip: int = 0, limit: int = 100):
    rooms = ControlRoom.get_Rooms(skip=skip, limit=limit)
    return rooms


#-------------------分享---------------
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
import urllib.request
import requests

def open_image_url(url:str):
    try:
        # 拆分URL
        parsed = urllib.parse.urlparse(url)

        # 获取路径部分,转换成本地地址
        path = parsed.path
        image = Image.open(f".{path}")
        return image

    except :
        print("_____不能打开"+url)

    



@router.post("/api/share", response_class=PlainTextResponse)
async def share(request: Request):
    data = await request.json()

    print(data)

    
    avatar_url = data.get("avatar_url")
    base_url =  "./static/img/back.jpg"
    share_url = "http://localhost:8000"+"/room/"+ data.get("share_url")



    

    # 下载头像和底图
    avatar = open_image_url(avatar_url)
    base = Image.open(base_url)

    #avatar = Image.open(avatar_url)
    #base = Image.open(base_url)

    # 调整头像大小
    avatar = avatar.resize((150, 150))

    # 在底图上添加头像
    base.paste(avatar, (base.width // 2 - avatar.width // 2, 50))

    # 在底图上添加文字 ，不需要写字，字直接在底图上写好。
    draw = ImageDraw.Draw(base)
    #font = ImageFont.truetype("getsmdl.ttf", 50)
    #text_width, text_height = draw.textsize(text, font)
    #draw.text((220, 250), "分享给朋友",font=font, fill=(0, 0, 0))

    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(share_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    print ("qr_img width:{},height:{}".format(qr_img.width,qr_img.height))

    # 在底图上添加二维码 位置也事先规定好。
    base.paste(qr_img, (585, 775))

    # 保存图片
    filename = "./static/img/share/{}_share.jpg".format(data.get("share_url"))
    base.save(filename)

    # 返回图片
    return "/static/img/share/{}_share.jpg".format(data.get("share_url"))
