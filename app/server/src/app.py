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
    return html_sub
