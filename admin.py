import os
import random
import uvicorn

from typing import Optional

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response ,RedirectResponse


from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
#from authlib.integrations.starlette_client import OAuth

from models.db import *

#from db import *

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        #测试，写死它
        if ("admin" == username) & ("dodo123" == password) :
                
            tokne = "faketoken"
            # Validate username/password credentials
            # And update session
            request.session.update({"token": tokne})

            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth
authentication_backend = AdminAuth(secret_key="惹不起")


app = FastAPI()
admin = Admin(app, engine,authentication_backend = authentication_backend)


class UserAdmin(ModelView, model=User):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    #显示方式
    column_list = [User.id, User.name,User.hash_password,User.egg,User.register_time,User.login_time,User.phone,User.email]
    column_details_exclude_list = [User.id]
    column_formatters = {User.name: lambda m, a: m.name[:16]}

    #功能
    column_searchable_list = [User.name,User.phone,User.email]
    column_sortable_list = [User.id,User.register_time,User.login_time]
    column_default_sort = [(User.login_time, True), (User.name, False)]
    
    #权限
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True

class RoomAdmin(ModelView, model=Room):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    #显示方式
    column_list = [Room.id, Room.title,Room.owner_id,Room.short_script,Room.create_time,Room.hotvalue,Room.eggvalue]
    column_details_exclude_list = [Room.id]
    column_formatters = {Room.title: lambda m, a: m.title[:10]}

    #功能
    column_searchable_list = [Room.title,Room.short_script,Room.long_script]
    column_sortable_list = [Room.id,Room.owner_id,Room.create_time,Room.hotvalue,Room.eggvalue]
    column_default_sort = [(Room.create_time, True), (Room.hotvalue, False)]
    
    #权限
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class MessageAdmin(ModelView, model=Message):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

 
    #显示方式
    column_list = [Message.id, Message.user_id,Message.room_id,Message.msg_q,Message.msg_a,Message.create_time]
    column_details_exclude_list = [Message.id]
    column_formatters = {
            Message.msg_a: lambda m, a: m.msg_a[:8]+"..",
            Message.msg_q: lambda m, a: m.msg_q[:8]+"..",
    }

    #功能
    column_searchable_list = [Message.msg_q,Message.msg_a]
    column_sortable_list = [Message.id,Message.user_id,Message.room_id,Message.create_time]
    column_default_sort = [(Message.create_time, True)]

    #权限
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class HistoryAdmin(ModelView, model=History):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    #显示方式
    column_list = [History.id,History.wtype,History.user_id,History.info,History.create_time]
    column_formatters = {History.info: lambda m, a: m.info[:10]}
    column_details_exclude_list = [History.id]

    #功能
    column_searchable_list = [History.info]
    column_sortable_list = [History.id,History.wtype,History.create_time]
    column_default_sort = [(History.create_time, True)]

    #权限
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class HistoryRoomAdmin(ModelView, model=HistoryRoom):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    #显示方式
    column_list = [HistoryRoom.id,HistoryRoom.wtype,HistoryRoom.user_id,HistoryRoom.room_id,HistoryRoom.info,HistoryRoom.create_time]
    column_formatters = {HistoryRoom.info: lambda m, a: m.info[:10]}
    column_details_exclude_list = [HistoryRoom.id]
 
    #功能
    column_searchable_list = [HistoryRoom.info]
    column_sortable_list = [HistoryRoom.id,HistoryRoom.wtype,HistoryRoom.create_time]
    column_default_sort = [(HistoryRoom.create_time, True)]

    #权限
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class HistoryMoneyAdmin(ModelView, model=HistoryMoney):
    def is_accessible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True

    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticatoinBackend
        return True
    #分页
    page_size = 50
    page_size_options = [25, 50, 100, 200]

 
    #显示方式
    column_list = [HistoryMoney.id,HistoryMoney.wtype,HistoryMoney.user_id,HistoryMoney.room_id,
                   HistoryMoney.money,HistoryMoney.egg,HistoryMoney.billNo,HistoryMoney.billNo_out,HistoryMoney.status,
                   HistoryMoney.info,HistoryMoney.create_time,
                  ]
    column_formatters = {HistoryMoney.info: lambda m, a: m.info[:10]}
    column_details_exclude_list = [HistoryMoney.id]

    #功能
    column_searchable_list = [HistoryMoney.info,HistoryMoney.billNo,HistoryMoney.billNo_out,HistoryMoney.status,HistoryMoney.money,HistoryMoney.egg]
    column_sortable_list = [HistoryMoney.id,HistoryMoney.wtype,HistoryMoney.create_time,HistoryMoney.status]
    column_default_sort = [(HistoryMoney.create_time, True)]
 
    #权限
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


admin.add_view(UserAdmin)
admin.add_view(RoomAdmin)
admin.add_view(MessageAdmin)
admin.add_view(HistoryAdmin)
admin.add_view(HistoryRoomAdmin)
admin.add_view(HistoryMoneyAdmin)



if __name__ == '__main__':
    uvicorn.run('admin:app', host='localhost', port=8001,reload=True)