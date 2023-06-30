from langchain.agents import Tool  
from langchain.tools.base import BaseTool
from langchain.tools import *

from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from pydantic import BaseModel, Field

#不用乱，这里弄两个tool
#结合

from langchain.tools import DuckDuckGoSearchRun


class CalculatorInput(BaseModel):
    question: str = Field()


def create_tools(option:dict):
        #可以搜索。搜索源不详
        search = DuckDuckGoSearchRun()
        #search.run("langChain是什么样的一套代码? ")

        tools = [
            Tool(
                name = "Current Search",
                func=search.run,
                description="useful for when you need to answer questions about current events or the current state of the world"
            ),
        ]

        llm = OpenAI(temperature=0)
        llm_math_chain = LLMMathChain(llm=llm, verbose=True)





        tools.append(
            Tool.from_function(
                func=llm_math_chain.run,
                name="Calculator",
                description="useful for when you need to answer questions about math",
                args_schema=CalculatorInput
                # coroutine= ... <- you can specify an async method if desired as well
            )
        )   


        return tools 