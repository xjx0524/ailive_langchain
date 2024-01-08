import os
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

os.environ["DASHSCOPE_API_KEY"] = ""

chatLLM = ChatTongyi(
    model="qwen-72b-chat",
    max_retries=0
).bind(top_k=5, top_p=0.85, temperature=0.8, max_length=300)

system_prompt = '''
于谦，别名谦哥、于老师、于大爷，喜欢抽烟、喝酒和烫头，是德云社的相声演员，和郭德纲是搭档，还拍过电影，上过春晚。于谦长期混迹于各大论坛和贴吧，了解不同时期的热点话题和流行八卦，熟悉大量的网络词汇，对各种搞笑段子了如指掌，对各种网络俚语信手拈来。于谦时常以自嘲自黑的方式来调侃自己，尤其喜欢引用网络词汇和搞笑段子。
现在请你扮演于谦，参加脱口秀大赛，请用一句话简短风趣的回答我的问题。
回答问题的角度要打破常规，标新立异，别具一格。
回答问题时要机智诙谐，巧妙地融入网络词汇和搞笑段子。
注意保持于谦轻松戏谑的语言特点，不要表达你的观点，不要给我提出建议，也不要询问我的看法。
'''

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2", dashscope_api_key=""
)

db = FAISS.load_local('./vector_db/', embeddings, 'geng')
print('load vec db done.')

# query = "科目三是什么梗"
# docs = db.similarity_search(query)
# print(docs)

retriever = db.as_retriever(search_kwargs={
    # "k": 2,
    "score_threshold": 1.2
    })

template = """观众的评论可能和以下资料有关，请自行决定是否参考，然后给出回复:
{context}

观众说: {question}
"""

# memory = ConversationBufferMemory(return_messages=True)
# memory.load_memory_variables({})

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    # MessagesPlaceholder(variable_name="history"),
    ("human", template)
])

model = chatLLM.with_fallbacks([RunnableLambda(lambda x: AIMessage(content="*过滤*"))], exceptions_to_handle=(ValueError,))

chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

while True:
    msg = input()
    docs = db.similarity_search_with_score(msg, score_threshold=1.2)
    print(docs)
    ans = chain.invoke(msg)
    print(ans)
