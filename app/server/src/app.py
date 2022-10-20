from flask import Flask
from flask_cors import CORS
from flask import request,jsonify
import requests
from bs4 import BeautifulSoup
import time
import re

app = Flask(__name__)
CORS(app,
    supports_credentials=True)

@app.route("/", methods=['GET'])
def index():
    print("test1")
    list = [
            {'text': "aaaa", 'color': "#eac645"},
            {'text': "baaaaka", 'color': "#ed4134"}
            ]
    return jsonify(results = list)

# 文章に形容詞か形状詞があれば意見とする
def ruleBaseFactCheck(str(sentence)):
    mecabTagger = MeCab.Tagger("mecabrc")
    node = mecabTagger.parseToNode(text)
    hcount = {}
    isOpinion = False
    while node:
        nshi = node.feature.split(",")[0]
        if hinshi == "形状詞" or hinshi == "形容詞":
            isTrue = True
            break
        node = node.next
    if isOpinion:
        return "#ff6347"#意見の場合 トマト色
    else :
        return "#f0e68c"#事実の場合 黄色


# ニュースを文章ごとに事実か意見か分ける
def isFackOrOpinion(str(text)):
    ret = []
    sentence_list = text.split("。")
    for sentence in sentence_list:
        result = ruleBaseFactCheck(sentence)
        ans = {}
        ans["text"] = sentence
        ans["color"] = result
        ret.append(ans)
    return ret


# URLからニュース記事をスクレイプ
# 今はYahooにのみ対応

@app.route("/test", methods=['POST'])
def test():
    print("test2")
    list = [
            {'text': "aaaa", 'color': "#eac645"},
            {'text': "baaaaka", 'color': "#ed4134"}
    ]

    url = request.json['url']
    print(url)
    return jsonify(results = list)


def newsExtraction(URL):
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
    return isFackOrOpinion(html_sub)
