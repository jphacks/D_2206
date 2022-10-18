from flask import Flask
from flask_cors import CORS
from flask import jsonify
import requests
from bs4 import BeautifulSoup
import time
import re

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/", methods=['GET'])
def index():
    list = [
            {'str': "aaaa", 'color': "yellow"},
            {'str': "baaaaka", 'color': "red"}
            ]
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
