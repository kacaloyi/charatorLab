from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from router.auth import check_token,pwd_context
from controls.control import ControlRoom,ControlChat,ControlUser

from sqlalchemy.orm import Session
from models.db import *
from models.schemas import *
#from models.models  import *
from conf.config import *
from utils.auth import *


router = APIRouter()




#注册
@router.post("/auth/regist")
async def regits(form_data: OAuth2PasswordRequestForm = Depends()):

    credentials_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="user name conflict",
        headers={"WWW-Authenticate": "Bearer"},
    )
    data = form_data
    print(data.username)
    print(data.password)
    #print(data.confirm_password)
    #if data.password != data.confirm_password:
    #    return {"statu":"error","info":"password are disaccord"}
    #检查用户名是否冲突
    user =ControlUser.get_user_by_name(data.username)
    if  user :
        raise credentials_exception
    
    #给password加密
    hash_password = pwd_context.hash(data.password)

    #在数据库中生成新的user记录。    
    user = ControlUser.create_user(dUserCreate(name=data.username,hash_password=hash_password))

    #返回结果
    return {"statu":"ok","info":"please login"}

#用usename和password直接登录,返回token，并且记录在cokie中。

@router.post("/auth/login")
async def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        detail="user name or password error",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = form_data
    #检查用户是否存在，
    #检查密码是否正确
    print(data.username)
    #print(data.password)
    #print(pwd_context.hash(data.password))

    #检查用户名是否冲突
    user =ControlUser.get_user_by_name(data.username)
    if not user :
        raise credentials_exception
    
    #print(user.hash_password)
    if not pwd_context.verify(data.password, user.hash_password):
        raise credentials_exception

    #生成token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires
    )

    data.password =None
    data.token = access_token
    '''
    for scope in data.scopes:
        print(scope)
    if data.client_id:
        print(data.client_id)
    if data.client_secret:
        print(data.client_secret)
    '''
    #返回包含token的数据。
    return {"statu":"ok","access_token": access_token, "token_type": "bearer"}


"""
#如果规定了response_mode，下面绑定的函数就要return一个同类型的返回值。
@app.post("/test/")#, response_model=schemas.tsModel)
def testmode(data: schemas.tsModel, db: Session = Depends(get_db)):
    print("进入test-:"+data.email+" "+data.password)
    return "hvqu"
# 4、创建您的FastAPI 路径操作
# 3、db: Session = Depends(get_db) ：当在路径操作函数中使用依赖项时，我们使用Session，直接从 SQLAlchemy 导入的类型声明它。
@app.post("/users/", response_model=schemas.dUser)
def create_user(user: schemas.dUserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
"""
#登出，网页端直接把令牌从cookie中删除就行了。服务器端不用管
@router.post("/auth/loginout")
async  def loginout(request:Request,current_user:User=Depends(check_token)):
    pass

#重置密码
@router.post("/auth/resetpass")
async def resetpass(fdata:resetPass,current_user:User=Depends(check_token)):

    if not pwd_context.verify(fdata.oldPassword, current_user.hash_password):
        return {"statu":"ok","info":"The old password is incorrect ","owner":current_user.id}

    if (not fdata.newPassword1) or (fdata.newPassword1 != fdata.newPassword2):
        return {"statu":"ok","info":"The new password is inconsistent ","owner":current_user.id}

    hash_password = pwd_context.hash(fdata.newPassword1)
    info = ControlUser.resetPasssword(current_user.id,hash_password)
    return {"statu":"ok","info":info,"owner":current_user.id} 

@router.post("/auth/resetavator")
async def restavator(fdata:resetAvator,current_user:User=Depends(check_token)):

    if not fdata.avator :
        return {"statu":"ok","info":"头像文件没有指认 ","owner":current_user.id}
    
    info = ControlUser.resetavator(current_user.id,fdata.avator) 
    return {"statu":"ok","info":info,"owner":current_user.id} 

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
def create_Room_for_user(room:dRoomCreate, current_user:User=Depends(check_token)):#room: schemas.dRoomCreate
    #print(room)
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

# 聊天，发送消息
@router.post("/api/chat", response_model=None)
async def chat(chatdata:dChartUser,  current_user:User=Depends(check_token)):
    generated = ControlChat.Chat(chatdata, current_user.id)
    return generated