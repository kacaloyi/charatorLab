from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi import Depends,Cookie,Header,Form, status, FastAPI, HTTPException,Request,File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from utils.exception import request_validation_exception_handler,register_middleware,register_exception


from conf.config import *
from utils.auth import *
from models.schemas import *  
from controls.control import *

router = APIRouter()


pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")



#register_exception(app)

class UnAuthorizedException( HTTPException):  
    def __init__(
        self,
    ) -> None:
        super().__init__(  
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    



@router.post("/auth/refresh_token")
def refresh_token(request: Request,response:Response,token = None):
    #从Head中读出token  
    #读不出来，就采用送进来的token，
    # 两个都没有，就是没有token，去登录  
 
    try :    
        cookies = request.cookies    
        token = cookies["token"]#转向登录
    except Exception :
        token = token
    
    if token == None :
        return {"statu":"fail"}   
    

    #解析出数据 ,检查是否过期,会自动做合法检测。比如有效期等。具体看jwt.decode()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        

        #print(payload)
        #token_data = TokenData(username=username)
    except JWTError:
        print("token unvalidable")
        return {"statu":"fail"}
    
    #检查用户名是否存在
    #print(payload)
    username: str = payload.get("sub")
    if username is None:
        return {"statu":"fail"}
    
    #刷新token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": payload.get("sub")}, expires_delta=access_token_expires
    )

    response.set_cookie("token",access_token)
    print("refresh_token:"+access_token)

    return {"statu":"ok","access_token": access_token, "token_type": "bearer"}
# 2、创建依赖项
# Dependency
#检查token
@router.post("/auth/check_token")
def check_token(request: Request,token = None):
    #从Head中读出token  
    #读不出来，就采用送进来的token，
    # 两个都没有，就是没有token，去登录  
 
    try :    
        cookies = request.cookies    
        token = cookies["token"]#转向登录
    except Exception :
        token = token
    
      


    if token == None :
        raise UnAuthorizedException()   
    
    print("check_token:"+token)       
    

    #解析出数据 ,检查是否过期,会自动做合法检测。比如有效期等。具体看jwt.decode()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        

        print(payload)
        #token_data = TokenData(username=username)
    except JWTError:
        print("token unvaliable")
        raise UnAuthorizedException()
    
    #检查用户名是否存在
    #print(payload)
    username: str = payload.get("sub")
    if username is None:
        #raise credentials_exception
        raise UnAuthorizedException()

    
    
    user = ControlUser.get_user_by_name(username)

    if user is None:
        raise UnAuthorizedException()
    #返回数据
    return user
        



#注册
@router.post("/auth/regist")
async def regits(form_data: OAuth2PasswordRequestForm = Depends()):

    credentials_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="user name conflict",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #data = form_data
    #print(data.username)
    #print(data.password)
    try:
        data = dUserLogin(name=form_data.username,password=form_data.password)# form_data
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}
    #print(data.confirm_password)
    #if data.password != data.confirm_password:
    #    return {"statu":"error","info":"password are disaccord"}
    #检查用户名是否冲突
    user =ControlUser.get_user_by_name(data.name)
    if  user :
        return {"statu":"fail","info":"user name conflict"}
        #raise credentials_exception
    
    #给password加密
    hash_password = pwd_context.hash(data.password)

    #在数据库中生成新的user记录。  
    try:  
        user = ControlUser.create_user(dUserCreate(name=data.name,hash_password=hash_password))
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}

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

    try:
        data = dUserLogin(name=form_data.username,password=form_data.password)# form_data
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}
    #检查用户是否存在，
    #检查密码是否正确
    #print(data.name)
    #print(data.password)
    #print(pwd_context.hash(data.password))

    #检查用户名是否冲突
    user =ControlUser.get_user_by_name(data.name)
    if not user :
        raise credentials_exception
    
    #print(user.hash_password)
    if not pwd_context.verify(data.password, user.hash_password):
        raise credentials_exception

    #生成token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.name}, expires_delta=access_token_expires
    )

    #data.password =None
    #data.token = access_token
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
async def resetpass(data:dict,current_user:User=Depends(check_token)):

    try:
        fdata = resetPass(oldPassword=data['oldPassword'],newPassword1=data['newPassword1'],newPassword2=data['newPassword2'])
    except ValueError as e:
        for error in e.errors():
            msg = error['msg']
            #msg字段(错误消息)和ctx字段(错误上下文)。
            # ctx = error['ctx']['xxx'] ctx字段包含原始的中文输入,
            return {"statu":"fail","info":msg}

    if not pwd_context.verify(fdata.oldPassword, current_user.hash_password):
        return {"statu":"fail","info":"The old password is incorrect ","owner":current_user.id}

    if (not fdata.newPassword1) or (fdata.newPassword1 != fdata.newPassword2):
        return {"statu":"fail","info":"The new password is inconsistent ","owner":current_user.id}

    hash_password = pwd_context.hash(fdata.newPassword1)
    info = ControlUser.resetPasssword(current_user.id,hash_password)
    return {"statu":"ok","info":info,"owner":current_user.id} 

@router.post("/auth/resetavator")
async def restavator(fdata:resetAvator,current_user:User=Depends(check_token)):

    if not fdata.avator :
        return {"statu":"ok","info":"头像文件没有指认 ","owner":current_user.id}
    
    info = ControlUser.resetavator(current_user.id,fdata.avator) 
    return {"statu":"ok","info":info,"owner":current_user.id}    
