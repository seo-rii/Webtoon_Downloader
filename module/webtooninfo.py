import json
import requests
import time
from bs4 import BeautifulSoup as bs4

import module.shared as shared
from module.gethtml import getRootHtml


def getWebtoonName(op, webtoonId, cookie):
    if op == 'naver' or op == 'nbest' or op == 'nchall':
        if shared.webtoonName == None:
            t = getRootHtml(op, webtoonId, cookie)
            try:
                soup = bs4(t, 'html.parser')
                shared.webtoonName = soup.find('meta', {"property": "og:title"})['content']
            except:
                shared.webtoonName = webtoonId
        return shared.webtoonName.replace('?', '')
    if op == 'daum':
        if shared.webtoonName == None:
            t = getRootHtml(op, webtoonId, cookie)
            try:
                js = json.loads(t)
                shared.webtoonName = js['data']['webtoon']['title']
            except:
                shared.webtoonName = webtoonId
        return shared.webtoonName.replace('?', '')
    if op == 'kakao':
        while True:
            try:
                td = requests.get("https://page.kakao.com/home?seriesId=" + webtoonId, cookies=cookie).text
            except:
                time.sleep(0.5)
                continue
            try:
                soup = bs4(td, 'html.parser')
                shared.webtoonName = soup.find('meta', {"property": "og:title"})['content']
            except:
                shared.webtoonName = webtoonId
            break
        return shared.webtoonName.replace('?', '')
