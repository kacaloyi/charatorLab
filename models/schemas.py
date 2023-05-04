from enum import IntEnum ,Enum
from typing import List, Union
from datetime import datetime
from models.db import roomType ,logType ,logTypeConsume,logTypeRoom


# 1、创建初始 Pydantic模型/模式
from pydantic import BaseModel,Field


# 1、创建初始 Pydantic模型/模式
class dRoomBase(BaseModel):
    title:str = "what's a rock room"
    sys_prompt:str = "what's amazement you want AI to do , as ..." #系统魔法

    short_script:str ="introduce your room"#短说明
    long_script:str  ="say more and detail"#长说明

    avatar :str ="the picture show your room"

    public :roomType  #True公开，任何人可以访问，false只有自己可以访问 

    #description: Union[str, None] = None

# 1、创建初始 Pydantic模型/模式
class  dRoomCreate( dRoomBase):
    owner_id :int = Field(...,title="creator id",description="创建者的ID")

    talking :str  = "怎样才能占领整个银河系"  #讨论主题
    bot_name :str = "AI勇士" #机器人名字
    hello :str    = "年轻人，来加入我们，为了世界和平" #见面第一句话
    categories:str= "test" # 类别

    sound :str    = "暂无" # 角色默认语音
    definition :str = "你是一个AI战士，你的任务是占领整个银河系。我是兵团指挥官，见到我要喊‘为了和平’" #高级定义
    


# 2、创建用于读取/返回的Pydantic模型/模式
class  dRoom( dRoomCreate):
    id :int = Field(...,title="room id") 

    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) #配图

    #owner = relationship("User",backref="my_room") 

    #这几样不能让用户编辑
    #create_time : datetime # = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间
    hotvalue :int # = Column(Integer, nullable=True,default =0) #热度
    eggvalue :int # = Column(Integer, nullable=True,default =0) #消耗

    class Config:
        orm_mode = True

class dRoomEdit(dRoomCreate):
    id:int = Field(...,title="room id") 
    class Config:
        orm_mode = True


# 1、创建初始 Pydantic模型/模式
class dUserBase(BaseModel):
    name: str

# 1、创建初始 Pydantic模型/模式
class dUserCreate(dUserBase):
    hash_password: str= Field(...,title="hash_password")  # = Column(String(80)) #加密后的密码

# 2、创建用于读取/返回的Pydantic模型/模式
class dUser(dUserBase):
    id :int #    = Column(Integer, primary_key=True,autoincrement = True)
    name :str = Field(...,title="name") #  = Column(String(16),unique=True, index=True)
    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) #头像配图
    avatar: str = Field("/static/img/face/face.png",title="avatar")
    
    
    phone : str #= Column(String(16),nullable=True,default ="")
    email : str #= Column(String(32),nullable=True,default ="")
    egg   : int #= Column(Integer, nullable=True,default =0) #金币
    actived :bool #      = Column(Boolean,nullable=True,default =True)  #false可以封号
    register_time :datetime # = Column(DateTime, nullable=True,default =  datetime.now) #创建时间
    login_time  :datetime #  = Column(DateTime, nullable=True,default = datetime.now) #最近登录时间
    #Rooms: List[ dRoom] = []

    class Config:
        orm_mode = True

class tsModel(BaseModel):
    email: str  #Field(None,description="email")
    password: str  #Field(None,description="password")

class resetPass(BaseModel):
    #8位 数字字母+特殊符号，不能是汉字。,regex ="/^(?![^a-zA-Z]+$)(?! D+$)(?![a-ZA-ZO-9]+$).{8,1$/"
    oldPassword:str = Field(...,title="oldPassword") 
    
    newPassword1:str = Field(...,title="password")
    newPassword2:str = Field(...,title="confirm password")
    
class resetAvator(BaseModel):
   avator:str = Field(...,title="avatar host url") 


class dChart(BaseModel):
    message:str = Field(...,title="发往服务器的信息")

class dChartUser(dChart):
    room_id:int = Field(...,title="房间号")
    role:str  = ""


class dChartBack(dChart):
    messageback:str = Field(...,title="服务器返还的信息")