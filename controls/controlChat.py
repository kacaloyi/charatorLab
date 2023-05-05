from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.db import User,Room,Message,session
from models.schemas import *

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile

from langchain.memory import ConversationBufferWindowMemory


from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from langchain.llms import OpenAI


class  ControlChat:
    #初始化的时候，建立与API的链接。断了重连？


    def Chat(chatdata:dChartUser, user:User):
        print (chatdata)
       
        #1 判断user是否合法，检查它egg是否还有
       
        #2 找到room，拼装prompty
        room = session.query( Room).filter(Room.id ==chatdata.room_id).first()
        #3 找到记忆的聊天记录，拼装prompty
        histroy = session.query(Message).filter(Message.room_id == chatdata.room_id, Message.user_id == user.id)\
                    .order_by(desc(Message.create_time))\
                    .limit(10).all()

        #4 发送给API

        #5 接受API返回信息，处理异常

        #6 解析返回信息，

        #7 处理消费

        #8 处理历史记录

        #9 拼装返回信息
        
    
        return room ,"收到了，虽然还不能对话，但是我看到你说什么了",0