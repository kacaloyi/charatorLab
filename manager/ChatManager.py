import time
from manager.define import Chat ,Singleton,DEAD_LIMIT
from manager.ChatFactory import ChatFactory



class ChatManager(metaclass=Singleton):
    def __init__(self):
        self.chatFactory =  ChatFactory()
        self.chats = {}

    def getChatbySessionid(self, sessionid):
        if sessionid not in self.chats:
            return None
            #self.chats[sessionid] =  self.chatFactory.createChat(sessionid,roomtlp,history,option)

        return self.chats[sessionid]
    
    def createChat(self,sessionid:str,room_template:str,histroy:list,option:dict):        
        self.poll(DEAD_LIMIT=DEAD_LIMIT)
        
        chat = self.chatFactory.createChat(sessionid=sessionid,roomtlp=room_template,history=histroy,option=option)
        self.chats[sessionid] = chat
        return chat

    def deleteChatBySessionid(self, sessionid):
        if sessionid in self.chats:
            del self.chats[sessionid]

    def poll(self, DEAD_LIMIT):
        now = time.time()
        for sessionid, chat in self.chats.items():
            if now - chat.lastupdatetime > DEAD_LIMIT:
                self.deleteChatBySessionid(sessionid)
