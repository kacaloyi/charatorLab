#一个文件写完增删查改

#运行测试
#uvicorn oneonly:app --reload

# 导入FastAPI模块
from fastapi import FastAPI
app = FastAPI()

# 1、连接mysql数据库需要导入pymysql模块
import pymysql
pymysql.install_as_MySQLdb()

# 2、配置数据库
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
SQLALCHEMY_DATABASE_URL = "mysql://test:123456@127.0.0.1:3306/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8')

# 3、把当前的引擎绑定给这个会话；
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = Session()

# 4、创建Base实例
# declarative_base类维持了一个从类到表的关系，通常一个应用使用一个Base实例，所有实体类都应该继承此类对象
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# 5、创建数据库模型（定义表结构:表名称，字段名称以及字段类型）
from sqlalchemy import Column, String, Integer

class User(Base):
    # 定义表名
    __tablename__ = 'user'
    # 定义字段
    # primary_key=True 设置为主键
    userid = Column(Integer, primary_key=True)
    username = Column(String(255))

    # 构造函数
    def __init__(self, userid, username):
        self.userid = userid
        self.username = username

    # 打印形式
    def __str__(self):
        return "id:%s, name:%s" % (str(self.userid), self.username)


# 6、在数据库中生成表
Base.metadata.create_all(bind=engine)

# 【增】
from pydantic import BaseModel
# 定义数据模型
class CreatUser(BaseModel):
    userid: int
    username: str

    def __str__(self):
        return "id：%s, name：%s" % (str(self.userid), self.username)

# 添加单个
@app.post("/user/addUser")
async def InserUser(user: CreatUser):
    try:
        # 添加数据
        dataUser = User(userid=user.userid, username=user.username)
        session.add(dataUser)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": "0000", "message": "添加成功"}


from typing import List


# 添加多个
@app.post("/user/addUserList")
async def addUserList(*, user: List[CreatUser]):
    try:
        # user是一个列表，每个内部元素均为CreatUser类型
        for u in user:
            # 自定义的数据模型可以用.访问属性
            dataUser = User(userid=u.userid, username=u.username)
            session.add(dataUser)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": "0000", "message": "添加成功"}


# 【查】

# 按照user_id查询
@app.get("/user/{user_id}")
async def queryUserByUserId(user_id: int):
    # 创建Query查询，filter是where条件，调用one返回唯一行，调用all则是返回所有行
    try:
        # one与first的区别：
        # one：要求结果集中只有一个结果；如果数据库返回0或2个或更多结果，并且将引发异常，则为错误。
        # first：返回可能更大的结果集中的第一个，如果没有结果，则返回None。不会引发异常。
        # filter_by与filter的区别：
        # filter_by接收的参数形式是关键字参数，而filter接收的参数是更加灵活的SQL表达式结构
        # user1 = session.query(User).filter_by(userid=user_id).first()
        user1 = session.query(User).filter(User.userid == user_id).first()
        session.close()
        # 由于user1只有一个值，所以它直接是一个字典
        if user1:
            return {"code": "0000", "message": "请求成功", "data": user1}
        else:
            return {"code": "0001", "message": "查询无结果"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


## 查询所有
@app.get("/user/selectall/")
async def queryUserByUserId():
    # 创建Query查询，filter是where条件，调用one返回唯一行，调用all则是返回所有行
    try:
        user1 = session.query(User).all()
        session.close()
        # user1 是一个列表，内部元素为字典
        return {"code": "0000", "message": "请求成功", "data": user1}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


#【删】

# 根据user_id删除单个
@app.delete("/user/deleteUser/{user_id}")
async def deleteUser(user_id: int):
    try:
        user1 = session.query(User).filter(User.userid == user_id).first()
        if user1:
            session.delete(user1)
            session.commit()
            session.close()
            return {"code": "0000", "message": "删除成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}


from typing import List


## 删除多个
@app.delete("/user/deleteUserList")
async def deleteUser(user_ids: List[int]):
    try:
        for user_id in user_ids:
            user1 = session.query(User).filter(User.userid == user_id).first()
            if user1:
                session.delete(user1)
                session.commit()
                session.close()
        return {"code": "0000", "message": "删除成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}


# 【改】

## 根据user_id修改user_name
@app.put("/user/updateUser/")
# 定义查询参数user_id和user_name
async def updateUser(user_id: int, user_name: str):
    try:
        user1 = session.query(User).filter(User.userid == user_id).first()
        print(user1)
        if user1:
            user1.username = user_name
            session.commit()
            session.close()
            return {"code": "0000", "message": "修改成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}


# 方式2：
class AlterUser(BaseModel):
    userid: int
    username: str


@app.put("/user/updateUser01/")
async def deleteUser(user: AlterUser):
    try:
        user1 = session.query(User).filter(User.userid == user.userid).first()
        if user1:
            user1.username = user.username
            session.commit()
            session.close()
            return {"code": "0000", "message": "修改成功"}
        else:
            return {"code": "0001", "message": "参数错误"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库错误"}

