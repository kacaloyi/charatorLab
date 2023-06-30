from manager.define import Chat

from langchain.agents import ConversationalChatAgent
from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain import OpenAI
from controls.utills.langPrompt import suffix,prefix
from controls.utills.langTools  import create_tools
from controls.utills.CustomOutputParser import CustomOutputParser

from langchain.agents.conversational_chat.prompt import (
    PREFIX,
    SUFFIX,
    TEMPLATE_TOOL_RESPONSE,
)

class ChatAgent(Chat):
    def __init__(self, sessionid,room_template,histroy,option):
        super().__init__(sessionid,room_template,histroy,option)


    @property
    def _agent_type(self) -> str:
        return "chat_agent"
    
    def _create_llm(self,option:dict):
        temperature = 0.7
        if 'temperature' in option:
            temperature = option['temperature']
        return OpenAI(temperature=temperature) 
    
    def _create_chat_llm(self,option:dict):
        temperature = 0.7
        if 'temperature' in option:
            temperature = option['temperature']
        return ChatOpenAI(temperature=temperature) 
    
    def _create_memery(self,history,option:dict):
        memory=ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True,k=6)

        for h in history:
            memory.save_context({"input": h.msg_q}, {"ouput":h.msg_a})

        return memory
    
    def _create_prompt_template(self,room_template):
        AGENT_PROMPT_prefix = room_template + prefix
        AGENT_PROMPT_suffix = suffix
        
        #Agent_TEMPLATE = room_template + """

        #    Current conversation:
        #    {history}
        #    Human: {input}
        #    AI:"""

        #AGENT_PROMPT = PromptTemplate(
        #        input_variables=["history", "input"], template=Agent_TEMPLATE
        #    )
        
        return AGENT_PROMPT_prefix,AGENT_PROMPT_suffix
    
    def _create_output_parser(self):

        return CustomOutputParser() 
    
    def _create_tools(self,room_template,option:dict):
        #这里生成tools[]

       

        return create_tools(option=option) 

    def _create(self,room_template:str,history:list,option:dict):
        #https://python.langchain.com/en/latest/modules/agents/agents/examples/chat_conversation_agent.html
        self.llm= self._create_llm(option=option)
        self.chat_llm = self._create_chat_llm(option=option)
        tools   = self._create_tools(room_template=room_template,option=option)

        prompts_prefix,promptes_suffix = self._create_prompt_template(room_template=room_template)
        print(prompts_prefix)
        print(promptes_suffix)


        prompt_tmp = ConversationalChatAgent.create_prompt(
            tools = tools,
            system_message=room_template,
            human_message=SUFFIX
        )

        print(prompt_tmp)

        
        self.memory  = self._create_memery(history=history,option=option)
        
 
        agent = ConversationalChatAgent.from_llm_and_tools(
            llm = self.chat_llm,
            tools= tools,
            system_message= room_template #"You are a helpful assistant. Answer as concisely as possible with a little humor expression."
        )
        from langchain.agents.agent import AgentExecutor

        self.agent_runner  = AgentExecutor.from_agent_and_tools (
            agent= agent,
            tools=tools,
            verbose=True, 
            memory=self.memory

        )

        return self.agent_runner
      
        self.agent_runner   =  initialize_agent(tools, self.chat_llm, 
                               agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
                               agent_kwargs = {"system_message":PREFIX,"human_message":SUFFIX,"input_variables":["input", "intermediate_steps", "chat_history"]},
                               verbose=True, 
                               memory=self.memory)

        #llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
        #agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

        return self.agent_runner

    def _predict(self, input:str):
        # do prediction here based on room type
        output = self.agent_runner.run(input=input)
        return output
    
    def clear(self):
        # do prediction here
        if self.memory is not None:
            self.memory.clear()
