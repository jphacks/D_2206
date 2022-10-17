from flask import Flask
import requests
from bs4 import BeautifulSoup
import time
import re

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello aaa"


def newsExtraction(URL):
    pattern = "<[^>]+>"

    bun_rest = requests.get(URL)
    bun_page = BeautifulSoup(bun_rest.text, "html.parser")
    html = bun_page.find_all("div",class_="article_body")
    html_sub = re.sub(pattern, "", str(html))
    # print(str(html))
    # print(html_sub)
    return html_sub
