#生成一个Chat类，属性变量有lastupdatetime，sessionid,成员函数有init，chat(input:str),getresult(),predict()

#另外生成一个ChatManager类，按sessionid管理Chat，有getChatbySessionid(),deleteChatBySessionid(),另外有个轮询函数，发现有Chat经过DEAD_LIMIT时间都没有更新了，就删除它。

#给ChatManager配套一个ChatFactory类，可以生成Chat。在ChatManager.get_chat_by_session_id()函数中如果找不到对应的Chat，就生成一个。
import time
from abc import ABC, abstractmethod


DEAD_LIMIT = 300 # 300秒

#用房间号和用户id，组合成一个唯一的session_id
def makeSesionID(roomid:int,userid:int):
    sessionid:str = str(roomid) + "_" + str(userid)
    return sessionid

#全局单例类
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


#对话聊天的基类
class Chat(ABC):
    def __init__(self, sessionid,room_template,histroy,option):
        self.lastupdatetime = time.time()
        self.sessionid = sessionid
        self.result = None
        self.chat = self._create(room_template=room_template,history=histroy,option=option)

    @abstractmethod
    def _create(self,room_template:str,history:list,option:dict):
        pass 

    @abstractmethod
    def _predict(self,input:str):
        # do prediction here
        pass

    @abstractmethod
    def clear(self):
        # do prediction here
        pass


    #input问话,返回回答
    def chatter(self, input:str):
        self.lastupdatetime = time.time()
        #self.result = self._predict(input)
        #return self.result["response"]
        output= self._predict(input)
        return output

    def getresult(self):
        return self.result

