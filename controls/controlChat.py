from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.db import User,Room,Message,session,HistoryMoney,HistoryRoom
from models.schemas import *

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile

from markdown import markdown

from langchain.memory import ConversationBufferWindowMemory


from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from langchain.llms import OpenAI


from manager.define import makeSesionID
from manager.ChatManager import ChatManager


chain : ConversationChain = None

class  ControlChat(ChatManager):
    def __init__(self):
        super().__init__()
    #初始化的时候，建立与API的链接。断了重连？

    def _make_session_id(self,room_id:int,user_id:int):
        return makeSesionID(roomid = room_id,userid = user_id )
    
    
    #按照设定的模板，加上Room信息，生成前半截prompt模板。
    def _make_room_prompt(self,room:int):
        from controls.utills.langPrompt import role

        return role.format(room=room) 
    
    #加载对应的聊天记录。
    def _load_history(self,roomid:int,userid:int):
        history = session.query(Message).filter(Message.room_id == roomid, Message.user_id == userid)\
                    .order_by(desc(Message.create_time))\
                    .limit(10).all()

        return history


    
    def _load_chatbot(self,chatdata:dChartUser,user:User):
        
        #2 找到room，拼装prompty
        room = session.query( Room).filter(Room.id ==chatdata.room_id).first()

        session_id = self._make_session_id(room_id=chatdata.room_id,user_id=user.id)
        chatbot = self.getChatbySessionid(sessionid=session_id)
        if None != chatbot :
            return chatbot ,room
        
        #2 找到room，拼装prompty       
        roomtlp = self._make_room_prompt(room=room)
        history = self._load_history(roomid=chatdata.room_id,userid=user.id)

        chatbot = self.createChat(sessionid=session_id,room_template=roomtlp,histroy=history,option={"type":"chain",'verbose':True})

        return chatbot ,room

    def load_chain(self,room:Room,user:User):
        global chain
        from controls.utills.langPrompt import PromptTemplate ,role,role_play_prompt

        mem = ConversationBufferWindowMemory()
        if chain is None:
            llm=ChatOpenAI()
            xchain = ConversationChain(
                llm=llm, 
                prompt = PromptTemplate(
                    input_variables=["history", "input"], template= role.format(room=room) +role_play_prompt
                    )  , 
                # We set a very low max_token_limit for the purposes of testing.
                #memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=40),
                memory=ConversationBufferWindowMemory(k=6),
                verbose=True,
               # room=room,
            )


            
            chain = xchain 

        return  chain 



    def Chat(self,chatdata:dChartUser, user:User):
        #print (chatdata)
       
        #1 判断user是否合法，检查它egg是否还有
        if (user.egg < 0) :
            room = session.query( Room).filter(Room.id ==chatdata.room_id).first()
            return   room ,markdown("***需要充值了" ) ,0
       
        #2 找到room，拼装prompty
        #room = session.query( Room).filter(Room.id ==chatdata.room_id).first()
        #3 找到记忆的聊天记录，拼装prompty
        #4 发送给API
        #5 接受API返回信息，处理异常
        #6 解析返回信息，
        #chain = self.load_chain(room,user)
        #output = chain.predict(input=chatdata.message)

        chat_bot,room = self._load_chatbot(chatdata=chatdata,user=user)
        print (chat_bot)
        print ("__________________________________________________________")

        from langchain.callbacks import get_openai_callback
        with get_openai_callback() as cb:
            output   = chat_bot.chatter(chatdata.message)
            print(output)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            #print(f"Total Cost (USD): ${cb.total_cost}")

        
        output = output
        print ("______==============================================________")
        #7 处理消费
        
        session.query(User).filter(id==user.id).update({User.egg:User.egg-cb.total_cost})
        mhis = HistoryMoney(wtype=logTypeConsume.consume,user_id = user.id,room_id = chatdata.room_id,info="聊天消耗",egg=cb.total_tokens,money=cb.total_cost)
        session.add(mhis)
        #rhis = HistoryRoom()

        #8 处理历史记录
        msg = Message(user_id = user.id,room_id=chatdata.room_id, msg_q = chatdata.message, msg_a = output )
        session.add(msg)
        session.commit()

        #9 拼装返回信息"
    
        return room ,markdown(output ) ,0
     
    #清除历史记录，删除Chat_bot，以后需要的时候重新加载
    def clear(self,room_id:int,user_id:int):

        sid = self._make_session_id(room_id=room_id,user_id = user_id)
        self.deleteChatBySessionid(sid) #删掉重来 
        #清空所有历史记录
        session.query(Message).filter(Message.room_id == room_id,Message.user_id == user_id).delete()
        return