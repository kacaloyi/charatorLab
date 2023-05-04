# backend.py
import os
import random
#依赖  
#  pip install python-jose[cryptography]
#  pip install passlib[bcrypt]
import uvicorn
from datetime import datetime, timedelta
from typing import List,Optional
from fastapi import Depends, FastAPI, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt 
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "b1985ef79dd1fd814890c5f5ba3fcd9e9eb1718e3ccc90837abcc5a554c7a11c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

       
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    #return User(
    #    username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    #)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"message": token}

#检查token
@app.post("/auth/check_token")
def check_token(request: Request):
    #从Head中读出token

    #解析出数据

    #检查是否过期

    #检查用户名是否存在

    #刷新过期值

    #返回数据
    pass

#注册
@app.post("/auth/regist")
def regits(form_data: OAuth2PasswordRequestForm = Depends()):

    credentials_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="user name conflict",
        headers={"WWW-Authenticate": "Bearer"},
    )
    data = form_data
    print(data.username)
    print(data.password)

    #检查用户名是否冲突
    user = get_user(fake_users_db,data.username)
    if  user :
        raise credentials_exception
    
    #给password加密

    #在数据库中生成新的user记录。    


    #返回结果
    return 

#用usename和password直接登录,返回token，并且记录在cokie中。
@app.post("/auth/login")
def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends()):

    data = form_data
    #检查用户是否存在，
    #检查密码是否正确
    print(data.username)
    print(data.password)

    #生成token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires
    )

    data.password =None
    data.token = access_token

    for scope in data.scopes:
        print(scope)
    if data.client_id:
        print(data.client_id)
    if data.client_secret:
        print(data.client_secret)

    #返回包含token的数据。
    return data






if __name__ == '__main__':
    uvicorn.run('miniServer:app', host='localhost', port=8000,reload=True)