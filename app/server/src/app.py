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


@app.route("/tfDetect", methods=['POST'])
def tfDetect():

    print("tfDetect")
    url = request.json['url']
    print(url)

    news_text = newsExtraction(url) #URL内のtextを抽出する
    texts = splitCiercle(news_text)#全文をlist型に「。」区切りで分割をする

    results = []
    for text in texts:
        ml_result = {}
        text = text + "。"
        #学習モデルにtextを読み込ませる
        ml_result['text'] = text
        if tof == '1':
            ml_result['color'] = "#eac645"
        else :
            ml_result['color'] = "#ed4134"
        results.append(ml_result)

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
    return html_sub

#「。」区切りで文章を分割するメソッド
def splitCiercle(texts):
    return texts.split("。")
