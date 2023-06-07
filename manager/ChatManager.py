import time
from manager.define import Chat ,Singleton,DEAD_LIMIT
from manager.ChatFactory import ChatFactory



class ChatManager(metaclass=Singleton):
    
    chatFactory =  ChatFactory()
    chats = {}

    def __init__(self):
        super().__init__()

    @classmethod
    def getChatbySessionid(cls, sessionid):
        if sessionid not in cls.chats:
            return None
            #self.chats[sessionid] =  self.chatFactory.createChat(sessionid,roomtlp,history,option)

        return cls.chats[sessionid]
    
    @classmethod
    def createChat(cls,sessionid:str,room_template:str,histroy:list,option:dict):        
        cls.poll(DEAD_LIMIT=DEAD_LIMIT)
        
        chat = cls.chatFactory.createChat(sessionid=sessionid,roomtlp=room_template,history=histroy,option=option)
        cls.chats[sessionid] = chat
        return chat

    @classmethod
    def deleteChatBySessionid(cls, sessionid):
        if sessionid in cls.chats:
            del cls.chats[sessionid]

    @classmethod
    def poll(cls, DEAD_LIMIT):
        now = time.time()
        for sessionid, chat in cls.chats.items():
            if now - chat.lastupdatetime > DEAD_LIMIT:
                cls.deleteChatBySessionid(sessionid)
