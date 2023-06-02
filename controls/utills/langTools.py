from langchain.agents import Tool  
from langchain.tools.base import BaseTool
from langchain.tools import *


#不用乱，这里弄两个tool
#结合

from langchain.tools import DuckDuckGoSearchTool
#可以搜索。搜索源不详
search = DuckDuckGoSearchTool()
#search.run("langChain是什么样的一套代码? ")

tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]