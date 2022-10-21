from flask import Flask
from flask_cors import CORS
from flask import request,jsonify
import requests
from bs4 import BeautifulSoup
import time
import re
from bertClassfier import BertClassifier

import numpy as np
import pandas as pd
# import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
# from transformers.modeling_bert import BertModel
from transformers import BertModel
# from transformers.tokenization_bert_japanese import BertJapaneseTokenizer
from transformers import BertJapaneseTokenizer
from transformers import BertModel
# from transformers import BertTokenizer
from transformers import AutoTokenizer
from torchtext.legacy import data
from transformers import BertTokenizer
from transformers import AutoTokenizer


app = Flask(__name__)
CORS(app,
    supports_credentials=True)
classifier = BertClassifier()
model_path = './model.pth'
classifier.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
MAX_LENGTH = 512
tokenizer = AutoTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
device = torch.device("cpu")
fact_color = "#000080"
opinion_color = "#f0e68c"


# 文章に形容詞か形状詞があれば意見とする
def ruleBaseFactCheck(text):
    mecabTagger = MeCab.Tagger("mecabrc")
    node = mecabTagger.parseToNode(text)
    hcount = {}
    isOpinion = False
    while node:
        hinshi = node.feature.split(",")[0]
        if hinshi == "形状詞" or hinshi == "形容詞":
            isTrue = True
            break
        node = node.next
    if isOpinion:
        return opinion_color#意見の場合 トマト色
    else :
        return fact_color#事実の場合 黄色

def bert_tokenizer(text):
    return tokenizer.encode(text, max_length=MAX_LENGTH, truncation=True, return_tensors='pt')[0]

def machineLearningBaseFactCheck(sentence):
    # classifier
    answer = []
    prediction = []

    text_tensor = bert_tokenizer(sentence)
    # numpyへ変換
    x_numpy = text_tensor.to('cpu').detach().numpy().copy()
    print(f'numpyへ変換:{x_numpy}')
    # 512になるまで末尾に0を追加
    for _ in range(512):
        if x_numpy.size < 512:
            x_numpy = np.append(x_numpy, 0)
    # print(f'512になるまで末尾に0を追加:{x_numpy}')

    #x_numpy = x_numpy.astype(np.float32)
    x_tensor = torch.from_numpy(x_numpy).clone()

    # print(x_tensor.shape)
    x_tensor = x_tensor.view(1,512)
    # print(x_tensor.shape)
    # print(f'最終整形:{x_tensor}')
    x_tensor = x_tensor.to(device)
    # print(f'最終形態:{x_tensor}')

    score, _ = classifier(x_tensor)
    _, pred = torch.max(score, 1)

    prediction += list(pred.cpu().numpy())
    #answer += list(label_tensor.cpu().numpy())
    # print(prediction[0])
    return fact_color if prediction[0] else opinion_color


# ニュースを文章ごとに事実か意見か分ける
def isFactOrOpinion(text):
    ret = []
    sentence_list = text.split("。")
    for sentence in sentence_list:
        # result = ruleBaseFactCheck(sentence)
        result = machineLearningBaseFactCheck(sentence)
        ans = {}
        ans["text"] = sentence
        ans["color"] = result
        ret.append(ans)
    return ret


# URLからニュース記事をスクレイプ
# 今はYahooにのみ対応
@app.route("/entryURL", methods=['POST'])
def newsExtraction():
    URL = request.json['url']
    # URL = "https://news.yahoo.co.jp/articles/59f7720e523b93fb002082feda885449700fa5e0"
    print(URL)
    pattern = "<[^>]+>"

    bun_rest = requests.get(URL)
    bun_page = BeautifulSoup(bun_rest.text, "html.parser")
    html = bun_page.find_all("div",class_="article_body")
    k = html[0].find_all("p",class_="sc-kaNhvL")
    if len(k) != 0:
        kill_html = str(html[0]).replace(str(k[0]),"")
    else:
        kill_html = str(html[0])
    html_sub = re.sub(pattern, "", kill_html)
    # print(str(html))
    # print(html_sub)
    result = isFactOrOpinion(html_sub)
    print(result)
    print(type(result))
    return jsonify(results = result)


@app.route("/", methods=['GET'])
def index():
    print("test1")
    list = [
            {'text': "aaaa", 'color': "#eac645"},
            {'text': "baaaaka", 'color': "#ed4134"}
            ]
    return jsonify(results = list)

# if __name__ == '__main__':
#     machineLearningBaseFactCheck("イギリスのトラス首相が就任わずか2ヵ月足らずで辞意を表明しました。")
