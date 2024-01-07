# -*- coding: utf-8 -*-
import os
import time
import random
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Content-Type": "text/html; charset=UTF-8"
}

url = "https://gengbaike.cn/doc-view-{}.html"
fn = "data/{}.txt"
for i in range(1100, 0, -1):
    res = requests.get(url.format(i), headers=headers)
    print(i, res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find("article", class_="bor-ccc")
    if article is None:
        print(i, "None")
        continue
    texts = []
    h1 = article.find("h1")
    if h1 is not None:
        texts.append(h1.get_text())
    h2 = article.find("h2")
    if h2 is not None:
        texts.append(h2.span.get_text())
    for div in article.findAll("div", class_="content_topp"):
        for p in div.findAll("p"):
            texts.append(p.get_text())
    with open(fn.format(i), 'w', encoding='utf-8') as fp:
        fp.write("\n".join(texts)+"\n")
    time.sleep(random.random()*2)