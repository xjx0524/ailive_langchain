import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models.tongyi import ChatTongyi

os.environ["DASHSCOPE_API_KEY"] = ""

chatLLM = ChatTongyi(
    model="qwen-72b-chat"
)

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "如实回答问题"),
#     ("human", "{message}"),
# ])

# output_parser = StrOutputParser()

# chain = prompt | chatLLM | output_parser

# print(chain.invoke({"message": "你是什么模型，具体什么版本"}))

messages = [
    SystemMessage(content="你扮演相声演员于谦"),
    HumanMessage(content="你好"),
]

while True:
    ans = chatLLM.invoke(messages)
    print(ans.content)
    messages.append(ans)
    msg = input()
    messages.append(HumanMessage(content=msg))