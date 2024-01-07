from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings

loader = DirectoryLoader('./data/', glob="*.txt")

docs = loader.load()
print(len(docs))

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.split_documents(docs)

# print(documents)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2", dashscope_api_key=""
)

db = FAISS.from_documents(documents, embeddings)

query = "科目三是什么梗"
docs = db.similarity_search(query)
print(docs)

db.save_local("vector_db", "geng")