
from langchain.prompts.prompt import PromptTemplate


role  = """你扮演{room.bot_name},这里是{room.title}。谈话的主题是{room.talking}, 
  {room.short_script}。
  {room.long_script},  
  {room.definition},
  开始第一句话:{room.hello} .  
  """

#role  = "你是个乐于助人的助手。用简练幽默的表现尽可能简短地回答。 "

role_play_prompt= """    

    Current conversation:
    {history}
    Human: {input}
    AI:"""

ROLE_PLAY_PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=role_play_prompt
    )



prefix = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:"""
suffix = """Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Args"

Question: {input}
{agent_scratchpad}"""


