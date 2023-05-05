from sqlalchemy.orm import Session

from models.db import User,Room,session
from models.schemas import *

 
class ControlUser: 
    def del_user(user_id:int):
        user =session.query(User).filter(User.id == user_id).first()
        print(user)
        if user:
            session.delete(user)
            session.commit()
        return user

    def get_user( user_id: int):
        return session.query( User).filter( User.id == user_id).first()

    # 通过电子邮件查询单个用户
    def get_user_by_email( email: str):
        return session.query( User).filter( User.email == email).first()

    # 通过用户名查询单个用户
    def get_user_by_name( name: str):
        return session.query( User).filter( User.name == name).first()

    # 查询多个用户
    def get_users(skip: int = 0, limit: int = 100):
        return session.query( User).offset(skip).limit(limit).all()

    def create_user(user: dUser):
        #fake_hashed_password = user.password + "notreallyhashed"
        # 使用您的数据创建一个 SQLAlchemy 模型实例。
        data_user =  User(name=user.name,hash_password=user.hash_password,avatar="/static/img/face/face.png")
        # 使用add来将该实例对象添加到您的数据库。
        session.add(data_user)
        # 使用commit来对数据库的事务提交（以便保存它们）。
        session.commit()
        # 使用refresh来刷新您的数据库实例（以便它包含来自数据库的任何新数据，例如生成的 ID）。
        session.refresh(data_user)
        return user
    
    def resetPasssword(user_id: int,hash_password:str):
        session.query( User).filter( User.id == user_id).update({"hash_password":hash_password})
        session.commit()

        return "ok"
    
    def resetavator(user_id,avator) :
        session.query( User).filter( User.id == user_id).update({"avatar":avator})
        session.commit()

        return "ok "

class ControlRoom:
    # 查询多个项目
    def get_rooms( skip: int = 0, limit: int = 100):
        rooms = session.query(Room).offset(skip).limit(limit).all()
        return rooms
    
    def get_room_by_id( roomid = 0):
        room =session.query( Room).filter(Room.id == roomid).first()
        return room
    
    def create_room(room:dRoomCreate,owner:dUser):
        data_room = Room(
            owner_id = owner.id, 
    
            title = room.title,
            sys_prompt = room.sys_prompt ,

            short_script = room.short_script ,
            long_script = room.long_script,
            avatar = room .avatar,
            public = room.public,

            talking  = room.talking,  #讨论主题
            bot_name = room.bot_name,  #机器人名字
            hello    = room.hello ,    #见面第一句话
            categories = room.categories, # 类别

            sound    = room.sound, # 角色默认语音
            definition  = room.definition,  #高级定义

        )


        session.add(data_room)
        session.commit()
        # 使用refresh来刷新您的数据库实例（以便它包含来自数据库的任何新数据，例如生成的 ID）。
        #session.refresh(data_room)

        nroom =session.query( Room).filter(Room.owner_id ==owner.id,Room.title == room.title).first()
        return nroom
    
    def edit_room(room:dRoomEdit,owner:dUser):
        
        session.query(Room).filter(Room.id == room.id,room.owner_id == owner.id ).update(room.dict())
        session.commit()
        
        
        return "ok"



