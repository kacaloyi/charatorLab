from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from router.auth import check_token,pwd_context
from controls.control import ControlRoom,ControlUser

from pydantic import ValidationError

from sqlalchemy.orm import Session
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
    
    return  {"statu":"ok","room":newroom,"owner":current_user.id}


# 编辑room，不能编辑历史资料
@router.post("/api/roomedit", response_model=None)
def create_Room_for_user(room: dRoomEdit, current_user:User=Depends(check_token)):
    if(room.owner_id!=current_user.id):
      return {"statu":"ok","info":"别人的room不能改","owner":current_user.id}
    
    ControlRoom.edit_room(room=room,owner=current_user)
    return {"statu":"ok","info":"ok","owner":current_user.id}

# 获取room表，可分页
@router.get("/api/roomlist/{skip}/{limit}", response_model=List[dRoom])
def read_Rooms(skip: int = 0, limit: int = 100):
    rooms = ControlRoom.get_Rooms(skip=skip, limit=limit)
    return rooms

