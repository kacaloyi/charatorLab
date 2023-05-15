from manager.define import Chat ,Singleton
#from manager.ChatManager import ChatManager
from manager.ChatAgent import ChatAgent
from manager.ChatChain import ChatChain


class ChatFactory:
    def __init__(self):
        #self.chatManager = ChatManager()
        return

    def createChat(self, sessionid, roomtlp,history,option):
        if option["type"] == "chain":
            chat = ChatChain(sessionid, roomtlp,history,option)
        elif option["type"] == "agent":
            chat = ChatAgent(sessionid, roomtlp,history,option)
        else:
            chat = Chat(sessionid)
        return chat



    def deleteChatBySessionid(self, sessionid):
        self.chatManager.deleteChatBySessionid(sessionid)

    def poll(self, DEAD_LIMIT):
        self.chatManager.poll(DEAD_LIMIT)
