import os
import sys
import requests
import gzip
import io
import json
import dashscope
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dashscope import BatchTextEmbedding
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings

#==================
# os.environ['OSS_ACCESS_KEY_ID'] = ''
# os.environ['OSS_ACCESS_KEY_SECRET'] = ''

# dashscope.api_key = ''

# loader = DirectoryLoader('./data/cuiuc/', glob="*.txt")

# docs = loader.load()
# print(len(docs))

# with open('tmp/docs.txt', 'w') as fp:
#     for d in docs:
#         fp.write(d.page_content.replace('\n', '\\n')+'\n')

# auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'xjx-pub')
# bucket.put_object_from_file('docs.txt', 'tmp/docs.txt')
# print('oss upload done.')

# file_url = "https://xjx-pub.oss-cn-beijing.aliyuncs.com/docs.txt"

# result = BatchTextEmbedding.call(BatchTextEmbedding.Models.text_embedding_async_v2,
#     url=file_url,
#     text_type="document")
# print(result)

# text_embeddings = []
# metadatas = []
# emb_map = {}
# if result.status_code == 200:
#     if result.output.task_status == 'SUCCEEDED':
#         print(result.output.url)
#         emb_response = requests.get(result.output.url)
#         if emb_response.status_code == 200:
#             # 使用 gzip 解压缩
#             with gzip.open(io.BytesIO(emb_response.content), 'rb') as f:
#                 content = f.read()
#                 embs = content.decode('utf-8').strip().split('\n')
#                 print(len(embs))
#                 assert len(embs) == len(docs)
#                 for i, e in enumerate(embs):
#                     data = json.loads(e)
#                     print(i, data['output']['text_index'])
#                     emb_map[data['output']['text_index']] = data['output']['embedding']
#             for i in range(len(docs)):
#                 text_embeddings.append((docs[i].page_content, emb_map[i]))
#                 metadatas.append(docs[i].metadata)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2", dashscope_api_key=""
)


# db = FAISS.from_embeddings(text_embeddings, embeddings, metadatas=metadatas)
# print('build index done.')

# db.save_local("vector_db", "cuiuc")
# print('save local done.')
#==================

db = FAISS.load_local('./vector_db/', embeddings, 'merge_20240109')

while True:
    query = input()
    docs = db.similarity_search_with_score(query, score_threshold=1.15)
    print(docs)

# db1 = FAISS.load_local('./vector_db/', embeddings, 'cuiuc')
# db2 = FAISS.load_local('./vector_db/', embeddings, 'geng')

# db1.merge_from(db2)
# db1.save_local("vector_db", "merge_20240109")