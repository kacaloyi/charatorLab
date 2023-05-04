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
        

    
