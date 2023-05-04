# 1、导入 SQLAlchemy 部件
from sqlalchemy import Column, Integer, String,Boolean,Text, Date,Enum,DateTime,ForeignKey,create_engine
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_fields.storages import FileSystemStorage
from sqlalchemy_fields.types import FileType, ImageType ,IPAddressType ,URLType

import enum
from datetime import datetime

# 连接mysql数据库需要导入pymysql模块
#import pymysql
#pymysql.install_as_MySQLdb()

# 2、为 SQLAlchemy 定义数据库 URL地址
# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
#SQLALCHEMY_DATABASE_URL = "mysql://test:123456@127.0.0.1:3306/test"

# 3、创建 SQLAlchemy 引擎
#engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8')

#使用sqlite ,python中内置Sqlite3，故无需安装第三方库，直接使用即可。

engine = create_engine(
    "sqlite:///D:/workspace/py/pyServerApp/database/example.db",#"sqlite:///database/example.db",
    connect_args={"check_same_thread": False},
)
# 4、创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    # 我们需要每个请求有一个独立的数据库会话/连接（SessionLocal），
    # 在所有请求中使用相同的会话，然后在请求完成后关闭它。
    db = SessionLocal()
    # 我们的依赖项将创建一个新的 SQLAlchemy SessionLocal，
    # 它将在单个请求中使用，然后在请求完成后关闭它。
    try:
        yield db
    finally:
        db.close()

# 实例化
session = SessionLocal()

# 5、创建一个Base类declarative_base
# 稍后我们将用这个类继承，来创建每个数据库模型或类（ORM 模型）
Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    #def date_format(value):
    #    return value.strftime("%h.%-%d.%m.%Y")
    #column_type_formatters = dict(ModelView.column_type_formatters, date=date_format)

    id     = Column(Integer, primary_key=True,autoincrement = True)
    name   = Column(String(16),unique=True, index=True)
    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) #头像配图
    avatar = Column(String(255),nullable=True,default ="")
    
    hash_password = Column(String(80)) #加密后的密码
    phone = Column(String(16),nullable=True,default ="")
    email = Column(String(32),nullable=True,default ="")
    egg   = Column(Integer, nullable=True,default =0) #金币
    actived       = Column(Boolean,nullable=True,default =True)  #false可以封号
    register_time = Column(DateTime, nullable=True,default =  datetime.now) #创建时间
    login_time    = Column(DateTime, nullable=True,default = datetime.now) #最近登录时间


    #def __repr__(self):
    #    return "name:{0} location:{1}".format(self.name,self.location)
#房间访问属性
class roomType (enum.Enum):
    public = "public"   #公开房间  public, private, linkable
    private = "private"   #私人房间，只能自己看
    linkable = "linkable"  #可以用链接访问，不出现在


class Room(Base):
    __tablename__ = "Rooms"

    id = Column(Integer, primary_key=True,autoincrement = True)
    title = Column(String(20),unique=True, index=True)
    talking  = Column(String(20)) #讨论主题
    bot_name = Column(String(20)) #机器人名字
    sys_prompt  = Column(String(255)) #系统魔法

    short_script  = Column(String(64)) #短说明
    long_script   = Column(String(255))  #长说明

    #avatar =  Column(ImageType(storage=FileSystemStorage(path="/pics"))) #配图
    avatar = Column(String(255),nullable=True,default ="")
    hello = Column(String(32)) #见面第一句话
    categories= Column(String(32)) # 类别

    public =  Column(Enum(roomType),nullable=True,default =roomType.public, index=True) #True公开，任何人可以访问，false只有自己可以访问

    owner_id =  Column(Integer,ForeignKey("Users.id"))#不是实体名，是table名。
    owner = relationship("models.db.User",backref="my_room") 
    
    sound = Column(String(20)) # 角色默认语音
    definition = Column(String(3200)) #高级定义

    create_time = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间
    hotvalue = Column(Integer, nullable=True,default =0) #热度
    eggvalue = Column(Integer, nullable=True,default =0) #消耗


#一次问答的聊天消息
class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True,autoincrement = True)

    user_id = Column(Integer,ForeignKey("Users.id"), index=True)
    room_id = Column(Integer,ForeignKey("Rooms.id"), index=True)
    user = relationship("models.db.User",backref="my_msg ") 
    room = relationship("models.db.Room",backref="room_msg")

    msg_q = Column(String(255), nullable=True,default ="")  #问,人类
    msg_a = Column(String(255), nullable=True,default ="")  #答,AI

    create_time = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间

#设置枚举值
class logType (enum.Enum):
    register = 1
    login    = 2 
    loginout = 3
    edit     = 4 #修改个人空间的简介形象等
    
    
    #其它
    other    = 999

class logTypeConsume(enum.Enum):
    #消费充值
    consume  = 80
    recharge = 81


class logTypeRoom(enum.Enum):
    #房间操作 创建 修改 进房间 出房间
    roomcreate = 60
    roomedit   = 61
    roomin     = 62
    roomout    = 63


#注册、修改、登入、登出、其它，等记录
class History(Base):
    __tablename__ = "Logs"
    id = Column(Integer, primary_key=True,autoincrement = True)
    wtype = Column(Enum(logType),nullable=True,default =logType.register, index=True)

    user_id = Column(Integer,ForeignKey("Users.id"), index=True)
    user = relationship("models.db.User",backref="my_history") 

    info = Column(String(255),default="")
    create_time = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间



#房间操作记录
class HistoryRoom(Base):
    __tablename__ = "LogsRoom"
    id = Column(Integer, primary_key=True,autoincrement = True)
    wtype = Column(Enum(logTypeRoom), nullable=True,default =logTypeRoom.roomin, index=True)

    user_id = Column(Integer,ForeignKey("Users.id"), index=True)
    user = relationship("models.db.User",backref="my_room_history") 

    info = Column(String(255),default="")
    create_time = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间

    room_id = Column(Integer,ForeignKey("Rooms.id"), nullable=True,default = 0, index=True)
    room = relationship("models.db.Room",backref="room_history")



#充值和消费，大厅roomid = 0 ,支付roomid = -1 
class HistoryMoney(Base):
    __tablename__ = "LogsMoney"
    id = Column(Integer, primary_key=True,autoincrement = True)
    wtype = Column(Enum(logTypeConsume),nullable=True,default =logTypeConsume.consume, index=True)

    user_id = Column(Integer,ForeignKey("Users.id"), index=True)
    user = relationship("models.db.User",backref="my_money_history") 

    info = Column(String(255),default="")
    create_time = Column(DateTime, nullable=True,default =  datetime.now, index=True)#创建时间

    room_id = Column(Integer,ForeignKey("Rooms.id"), nullable=True,default = 0, index=True)
    room = relationship("models.db.Room",backref="room_money_history")
    
    money = Column(Integer,nullable = True ,default = 0) 
    egg   = Column(Integer)  #消费为负值，奖励为正值，原因在info中说明

    #账单号，内部账单号，账单处理状态
    billNo = Column(String(64), nullable=True,default = "", index=True)
    billNo_out = Column(String(64), nullable=True,default = "", index=True)
    status = Column(Integer, nullable=True,default = 0, index=True)




#临时写的，现在在不断地改库，重启就清空数据库，重新生成新库。
#Base.metadata.drop_all(engine) 
#sql = 'DROP TABLE IF EXISTS Room;'
#result = engine.execute(sql)

Base.metadata.create_all(engine)  # Create tables