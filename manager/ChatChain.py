from manager.define import Chat

from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)

from controls.utills.langPrompt import role_play_prompt


#以Chat为基类，衍生ChatChain类和ChatAgent类。 
#前面的代码改写，生成Chat的时候，送入一个参数class Room,依据Room.type的不同，生成不同的Chat子类，但是由ChatManager统一管理。

 
class ChatChain(Chat):
    def __init__(self, sessionid,room_template,histroy,option):
        super().__init__(sessionid,room_template,histroy,option)

    def _create_llm(self,option:dict):
        temperature = 0.7
        if 'temperature' in option:
            temperature = option['temperature']
        return ChatOpenAI(temperature=temperature) 
    
    def _create_prompt_template(self,room_template):#Current conversation:
        CHAIN_TEMPLATE ="The following is a friendly conversation between a human and an AI."+ room_template + role_play_prompt 

        CHAIN_PROMPT = PromptTemplate(
                input_variables=["history", "input"], template=CHAIN_TEMPLATE
            )
        
        return CHAIN_PROMPT
    """def _create_prompt_template(self,room_template):#Current conversation:
        prompt = ChatPromptTemplate.from_messages([

        #SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
        SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI."+room_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        return prompt  """
    
    def _create_memery(self,history,option:dict):
        memory=ConversationBufferWindowMemory(k=6)
        for h in history:
            memory.save_context({"input": h.msg_q}, {"ouput":h.msg_a})

        return memory
    
    def _create(self,room_template:str,history:list,option:dict):
        llm = self._create_llm(option) 
        memory = self._create_memery(history=history,option=option)
        tlp    = self._create_prompt_template(room_template=room_template)

        verbose = False
        if 'verbose' in option and option['verbose']!=False :
            verbose = True

        chat = ConversationChain(
            llm=llm, 
            prompt = tlp,
            # We set a very low max_token_limit for the purposes of testing.
            #memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=40),
            memory=memory,
            verbose=verbose,
        )

        return chat 
        

    def _predict(self, input:str):
        # do prediction here based on room type
        print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        output = self.chat.predict(input=input)
        
        return output
    
    
    def clear(self):
        # do prediction here
        if self.chat is not None:
            self.chat.memory.clear()
        