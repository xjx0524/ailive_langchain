import os
import sys
import requests
import gzip
import io
import json
import dashscope
from dashscope import BatchTextEmbedding
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings

dashscope.api_key = 'sk-'

loader = DirectoryLoader('./data/cuiuc/', glob="19[0-9][0-9].txt")

docs = loader.load()
print(len(docs))

# text_splitter = CharacterTextSplitter(
#     separator="\n\n",
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len,
#     is_separator_regex=False,
# )

# documents = text_splitter.split_documents(docs)

# print(documents)

# with open('tmp/docs.txt', 'w') as fp:
#     for d in docs:
#         fp.write(d.page_content.replace('\n', '\\n')+'\n')

# file_url = "https://xjx-pub.oss-cn-beijing.aliyuncs.com/docs.txt"

# result = BatchTextEmbedding.call(BatchTextEmbedding.Models.text_embedding_async_v2,
#     url=file_url,
#     text_type="document")
# print(result)


# if result.status_code == 200:
#     if result.output.task_status == 'SUCCEEDED':
#         print(result.output.url)
#         emb_response = requests.get(result.output.url)
#         if emb_response.status_code == 200:
#             # 使用 gzip 解压缩
#             with gzip.open(io.BytesIO(emb_response.content), 'rb') as f:
#                 content = f.read()
#                 emb = json.loads(content.strip())
#                 print(emb)

text_embeddings = []
metadatas = []

res_url = "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/5fc5c860/2024-01-09/2ef33d78-29f8-4289-acf4-e1273c5d0285_output_1704794062989.txt.gz?Expires=1705053263&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=YW4SYPQ5MOpNFGDkbDex%2Fl61SqA%3D"
emb_response = requests.get(res_url)
if emb_response.status_code == 200:
    # 使用 gzip 解压缩
    with gzip.open(io.BytesIO(emb_response.content), 'rb') as f:
        content = f.read()
        embs = content.decode('utf-8').strip().split('\n')
        print(len(embs))
        assert len(embs) == len(docs)
        for i, e in enumerate(embs):
            data = json.loads(e)
            print(i, data['output']['text_index'])
            text_embeddings.append((docs[i].page_content, data['output']['embedding']))
            metadatas.append(docs[i].metadata)


# embeddings = DashScopeEmbeddings(
#     model="text-embedding-v2", dashscope_api_key="sk-"
# )

# db = FAISS.from_documents(documents, embeddings)

# db = FAISS.from_embeddings(text_embeddings, embeddings, metadatas=metadatas)

# db = FAISS.load_local('./vector_db/', embeddings, 'test')

# query = "尼康战歌"
# docs = db.similarity_search_with_score(query)
# print(docs)

# db.save_local("vector_db", "test")
