from enum import IntEnum ,Enum 
from typing import List, Union
from datetime import datetime
from models.db import roomType ,logType ,logTypeConsume,logTypeRoom


# 1、创建初始 Pydantic模型/模式
from pydantic import BaseModel,Field, validator, EmailStr,constr, HttpUrl, FilePath

# 1、创建初始 Pydantic模型/模式
class dRoomBase(BaseModel):
    title:str       =  Field("多棒的小屋", title="talking", max_length=20, description="房间招牌") #房间招牌
    sys_prompt: str = Field("你想让AI做点儿什么惊奇的事儿, 比如 ...", title="sys_prompt", max_length=255, description="系统魔法")

    short_script: str = Field("介绍你的房间", title="short_script", max_length=64, description="短说明")
    long_script: str  = Field("详细说明房间规则", title="long_script", max_length=255, description="长说明")

    avatar: str     = Field("/static/img/face/face.png", title="avatar", max_length=255, description="使用的头像")

    public: roomType = Field(roomType.public,title="开放程度",description="开放程度") #True公开，任何人可以访问，false只有自己可以访问 
    @validator('public', allow_reuse=True)
    def validate_public(v):
        if v not in roomType.__members__.values():
            raise ValueError('必须是%s中的一个值' % ','.join(roomType.__members__.keys()))
        return v

    @validator('title', 'sys_prompt', 'short_script', 'long_script', 'avatar')
    def no_injection(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        return v

    # 校验不允许有注入攻击

# 1、创建初始 Pydantic模型/模式
class  dRoomCreate( dRoomBase):
    owner_id :int = Field(...,title="creator id",description="创建者的ID")

    talking :str  = Field("怎样才能占领整个银河系", title="talking", max_length=20, description="讨论主题")
    bot_name :str = Field("AI勇士", title="bot_name", max_length=20, description="机器人名字")
    hello :str    = Field("年轻人，来加入我们，为了世界和平", title="hello", max_length=32, description="见面第一句话")
    categories:str= Field("test", title="categories", max_length=32, description="类别")

    sound :str    = Field("暂无", title="sound", max_length=20, description="角色默认语音")
    definition :str = Field("你是一个AI战士，你的任务是占领整个银河系。我是兵团指挥官，见到我要喊‘为了和平’", title="definition", max_length=3000, description="高级定义")

    @validator('talking', 'bot_name', 'hello', 'categories', 'sound', 'definition')
    def no_injection(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        return v
    


# 2、创建用于读取/返回的Pydantic模型/模式
class  dRoom( dRoomCreate):
    id :int = Field(...,title="room id",description="房间的ID") 

    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) #配图

    #owner = relationship("User",backref="my_room") 

    #这几样不能让用户编辑
    #create_time : datetime # = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间
    hotvalue :int # = Column(Integer, nullable=True,default =0) #热度
    eggvalue :int # = Column(Integer, nullable=True,default =0) #消耗

    class Config:
        orm_mode = True

class dRoomEdit(dRoomCreate):
    id:int = Field(...,title="room id",description="房间的ID") 
    class Config:
        orm_mode = True


# 1、创建初始 Pydantic模型/模式
class dUserBase(BaseModel):
    name: str
    @validator('name')
    def username_valid(cls, v):
        if not v.isalnum():
            raise ValueError('用户名必须是字母加数字')
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if len(v) < 6 or len(v) > 16:
            raise ValueError('用户名长度必须在6个以上，不能超过16个')
        return v

class dUserLogin(dUserBase):
    password:str 
    @validator('password')
    def username_valid(cls, v):
        if not v.isalnum():
            raise ValueError('密码必须是字母加数字')
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if len(v) < 4 or len(v) > 16:
            raise ValueError('密码长度必须在4个以上，不能超过16个')
        return v


# 1、创建初始 Pydantic模型/模式
class dUserCreate(dUserBase):
    hash_password: str= Field(...,title="hash_password")  # = Column(String(80)) #加密后的密码

    @validator('hash_password')
    def no_injection(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if len(v) > 79:
            raise ValueError('hash_password长度不能超过80个')
        return v

# 2、创建用于读取/返回的Pydantic模型/模式
class dUser(dUserBase):
    id :int #    = Column(Integer, primary_key=True,autoincrement = True)
    name :str = Field(...,title="name") #  = Column(String(16),unique=True, index=True)
    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) 
    avatar: str = Field("/static/img/face/face.png",title="avatar")#头像配图
    
    
    phone : str #= Column(String(16),nullable=True,default ="")#手机号
    email : str #= Column(String(32),nullable=True,default ="")#邮箱
    egg   : int #= Column(Integer, nullable=True,default =0) #金币
    actived :bool #      = Column(Boolean,nullable=True,default =True)  #是否已激活,false可以封号
    register_time :datetime # = Column(DateTime, nullable=True,default =  datetime.now) #创建时间
    login_time  :datetime #  = Column(DateTime, nullable=True,default = datetime.now) #最近登录时间
    #Rooms: List[ dRoom] = []

    class Config:
        orm_mode = True

class tsModel(BaseModel):
    email: str  #Field(None,description="email")
    password: str  #Field(None,description="password")

    @validator('email')
    def email_valid(cls, v):
        if not v.count('@') == 1:
            raise ValueError('邮箱地址必须是有效的邮箱地址格式')
        return v
    @validator('password')
    def password_valid(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if not v.isalnum():
            raise ValueError('密码必须是字母加数字')
        if not any(char.isupper() for char in v):
            raise ValueError('密码必须有大写字母')
        if len(v) < 6 or len(v) > 10:
            raise ValueError('密码长度必须在6个以上，不能超过10个')
        return v

class resetPass(BaseModel):
    #8位 数字字母+特殊符号，不能是汉字。,regex ="/^(?![^a-zA-Z]+$)(?! D+$)(?![a-ZA-ZO-9]+$).{8,1$/"
    oldPassword:str = Field(...,title="oldPassword") 
    
    newPassword1:str = Field(...,title="password")
    newPassword2:str = Field(...,title="confirm password")

    @validator('oldPassword')
    def oldPassword_valid(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if len(v) < 1 or len(v) > 16:
            raise ValueError('写入正确的旧密码')
        return v

    @validator('newPassword1','newPassword2')
    def password_valid1(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if not v.isalnum():
            raise ValueError('新密码必须是字母加数字')
        if not any(char.isupper() for char in v):
            raise ValueError('新密码必须有大写字母')
        if len(v) < 6 or len(v) > 16:
            raise ValueError('新密码长度必须在6个以上，不能超过16个')
        return v
    
   
    
class resetAvator(BaseModel):
   avator:str = Field(...,title="avatar host url") 


class dChart(BaseModel):
    message:str = Field(...,title="发往服务器的信息")

    @validator('message')
    def message_valid(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('不允许注入攻击')
        if len(v) > 1000:
            raise ValueError('hash_password长度不能超过1000个')
        return v

class dChartUser(dChart):
    room_id:int = Field(...,title="房间号")
    role:str  = ""


class dChartBack(dChart):
    messageback:str = Field(...,title="服务器返还的信息")