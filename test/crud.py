from sqlalchemy.orm import Session

import models, schemas

def del_user(db:Session,user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    if user:
        db.delete(user)
        db.commit()
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 通过 ID 和电子邮件查询单个用户
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 查询多个用户
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    fake_hashed_password = user.password + "notreallyhashed"
    # 使用您的数据创建一个 SQLAlchemy 模型实例。
    db_user = models.User(email=user.email,password=fake_hashed_password)
    # 使用add来将该实例对象添加到您的数据库。
    db.add(db_user)
    # 使用commit来对数据库的事务提交（以便保存它们）。
    db.commit()
    # 使用refresh来刷新您的数据库实例（以便它包含来自数据库的任何新数据，例如生成的 ID）。
    db.refresh(db_user)
    return user

# 查询多个项目
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return item
