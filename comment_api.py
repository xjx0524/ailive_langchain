import json
from pydantic import BaseModel, root_validator, model_validator
import requests
import base64
import time
from typing import List, Optional

class Comment(BaseModel):
    commentId: int
    content: str
    liveId: Optional[int] = None
    publisherNick: str
    enhancedType: Optional[str] = None   # 'follow'表示关注
    timestamp: Optional[int] = None      # 发布时间戳 毫秒

    @model_validator(mode="before")
    def extract_enhancedType(cls, values):
        renders_info = values.get('renders')
        if renders_info and 'enhancedType' in renders_info:
            values['enhancedType'] = renders_info['enhancedType']
        return values

def get_comments(topic):
    url = "https://impaas.alicdn.com/live/message/" + topic + "/0/" + str(int(time.time()))
    print(url)
    # 发起GET请求
    response = requests.get(url)
    #print(response.text)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的内容为JSON
        data = response.json()
        for comment_data in data["payloads"]:
            # 解码 Base64 字符串
            decoded_bytes = base64.b64decode(comment_data["data"])
            # 将解码后的字节转换成字符串
            decoded_str = decoded_bytes.decode('utf-8')
            data_json = json.loads(decoded_str)
            #print(data_json)
            comment = Comment.model_validate_json(decoded_str)
            print(comment)
        #print(data)
    else:
        print(f'请求失败，状态码为: {response.status_code}')


if __name__ == '__main__':
    #url = "https://impaas.alicdn.com/live/message/dd49cc3c-53db-46c9-a44e-66bd5d8b399f/0/1704787221"
    get_comments("dd49cc3c-53db-46c9-a44e-66bd5d8b399f")
    #get_comments("84950989-ca0f-443e-b7f4-d0edc368adda")