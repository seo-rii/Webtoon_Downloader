from bs4 import BeautifulSoup as bs4
from multiprocessing import Process, freeze_support, Array, Queue, Value
import requests
from urllib.parse import urlparse, parse_qs
import os
from PIL import Image
import re
import sys
import shutil
import time
import json

class NCookie:
    def __init__(self, auth, sess):
        self._auth=auth
        self._sess=sess

class DCookie:
    def __init__(self, hm_cu, hts, prof, ts, lsid):
        self._hm_cu=hm_cu
        self._hts=hts
        self._prof=prof
        self._ts=ts
        self._lsid=lsid

def log(str, lv=2):
    if lv>1:
        print(str)
        sys.stdout.flush()

def makeUrl(op, webtoonId, viewNo=0):
    if op=='naver':
        return "https://comic.naver.com/webtoon/detail.nhn?titleId="+str(webtoonId)+"&no="+str(viewNo)
    if op=='nbest':
        return "https://comic.naver.com/bestChallenge/detail.nhn?titleId="+str(webtoonId)+"&no="+str(viewNo)
    if op=='nchall':
        return "https://comic.naver.com/challenge/detail.nhn?titleId="+str(webtoonId)+"&no="+str(viewNo)
    if op=='daum':
        return "http://webtoon.daum.net/data/pc/webtoon/viewer_images/"+str(webtoonId)

def makeRootUrl(op, webtoonId):
    if op=='naver':
        return "https://comic.naver.com/webtoon/list.nhn?titleId="+str(webtoonId)
    if op=='nbest':
        return "https://comic.naver.com/bestChallenge/list.nhn?titleId="+str(webtoonId)
    if op=='nchall':
        return "https://comic.naver.com/challenge/list.nhn?titleId="+str(webtoonId)
    if op=='daum':
        return "http://webtoon.daum.net/data/pc/webtoon/view/"+str(webtoonId)

def getRootHtml(op, webtoonId):
    try:
        t=requests.get(makeRootUrl(op, webtoonId)).text
    except:
        t=-1
    return t

def getRootHtmlDaemon(op, webtoonId):
    global rootHtml
    if 'rootHtml' in globals():
        return rootHtml
    while True:
        td=getRootHtml(op, webtoonId)
        if td==-1:
            time.sleep(0.5)
            continue
        rootHtml=td
        return td

def getWebtoonName(op, webtoonId):
    global webtoonName
    if op=='naver' or op=='nbest' or op=='nchall':
        if not 'webtoonName' in globals():
            t=getRootHtmlDaemon(op, webtoonId)
            try:
                soup = bs4(t, 'html.parser')
                webtoonName=soup.find('meta', {"property":"og:title"})['content']
            except:
                webtoonName=webtoonId
        return webtoonName
    if op=='daum':
        if not 'webtoonName' in globals():
            t=getRootHtmlDaemon(op, webtoonId)
            try:
                js=json.loads(t)
                webtoonName=js['data']['webtoon']['title']
            except:
                webtoonName=webtoonId
        return webtoonName

def getRawHtml(op, webtoonId, cookie, viewNo=0):
    cookies=dict()
    if cookie!=None:
        if op=='naver':
            cookies = {'NID_AUT': cookie._auth, 'NID_SES':cookie._sess}
        if op=='daum':
            cookies = {'HM_CU': cookie._hm_cu, 'HTS':cookie._hts, 'PROF':cookie._prof, 'TS':cookie._ts, 'LSID':cookie._lsid}
    else:
        cookies=None
    try:
        t=requests.get(makeUrl(op, webtoonId, viewNo), cookies=cookies).text
    except:
        t=-1
    return t

def getRawHtmlDaemon(op, webtoonId, cookie, viewNo=0):
    if viewNo==-1:
        return -1
    while True:
        td=getRawHtml(op, webtoonId, cookie, viewNo)
        if td==-1:
            time.sleep(0.5)
            continue
        return td

def getRawEpisodeNo(html):
    soup = bs4(html, 'html.parser')
    try:
        return parse_qs(urlparse(soup.find('meta', {"property":"og:url"})['content']).query)['no'][0]
    except:
        return -1

def getFinCode(op, webtoonId, cookie):
    global fincode
    if 'fincode' in globals():
        return fincode
    fincode=getRawEpisodeNo(getRawHtmlDaemon(op, webtoonId, cookie, 0))
    return fincode

def getHtml(op, webtoonId, viewNo, cookie):
    global html
    global reIndex
    global htmlLst
    if not 'html' in globals():
        html=dict()
    if not 'reIndex' in globals():
        reIndex=[0]
    if op=='naver' or op=='nbest' or op=='nchall':
        for findFor in range(len(reIndex), viewNo+2):
            for i in range(reIndex[findFor-1]+1, int(getFinCode(op, webtoonId, cookie))+2):
                tmpHtml=getRawHtmlDaemon(op, webtoonId, cookie, i)
                if getRawEpisodeNo(tmpHtml)==str(i):
                    reIndex.append(i)
                    html.update({len(reIndex)-1:tmpHtml})
                    break
        return html[viewNo]
    if op=='daum':
        if not 'htmlLst' in globals(): 
            htmlLst=list()
            t=getRootHtmlDaemon(op, webtoonId)
            js=json.loads(t)
            webtoonLinks=js['data']['webtoon']['webtoonEpisodes']
            lst=list()
            for i in webtoonLinks:
                if i['serviceType']=='free':
                    lst.append(i['articleId'])
            lst.append(-1)
            lst.reverse()
            for i in lst:
                try:
                    t=getRawHtmlDaemon(op, i, cookie)
                except:
                    t=-1
                htmlLst.append(t)
        return htmlLst[int(viewNo)]


def getImgNo(op, webtoonId, viewNo, cookie):
    global imgUrl
    global imgNo
    if not 'imgUrl' in globals():
        imgUrl=dict()
    if not 'imgNo' in globals():
        imgNo=dict()
    if (op=='naver' or op=='nbest' or op=='nchall') and (not 'html' in globals() or not viewNo in html):
        getHtml(op, webtoonId, viewNo, cookie)
    if (op=='daum') and (not 'htmlLst' in globals() or not viewNo in html):
        getHtml(op, webtoonId, viewNo, cookie)
    if op=='naver' or op=='nbest' or op=='nchall':
        soup = bs4(html[viewNo], 'html.parser')
        for img_tag in soup.select('.wt_viewer img'):
            if not viewNo in imgUrl:
                imgUrl.update({viewNo:list()})
            imgUrl[viewNo].append(img_tag['src'])
        imgNo.update({viewNo:len(soup.select('.wt_viewer img'))})
        return len(soup.select('.wt_viewer img'))
    if op=='daum':
        js=json.loads(htmlLst[viewNo])
        for img_tag in js['data']:
            if not viewNo in imgUrl:
                imgUrl.update({viewNo:list()})
            imgUrl[viewNo].append(img_tag['url'])
        imgNo.update({viewNo:len(js['data'])})
        return len(js['data'])

def downImg(op, webtoonId, viewNo, cutNo, cookie):
    if not 'imgUrl' in globals() or not viewNo in imgUrl:
        getImgNo(op, webtoonId, viewNo, cookie)
    cookies=dict()
    if cookie!=None:
        if op=='naver':
            cookies = {'NID_AUT': cookie._auth, 'NID_SES':cookie._sess}
        if op=='daum':
            cookies = {'HM_CU': cookie._hm_cu, 'HTS':cookie._hts, 'PROF':cookie._prof, 'TS':cookie._ts, 'LSID':cookie._lsid}
    else:
        cookies=None
    headers = {'Referer': makeUrl(op, webtoonId, viewNo)}
    try:
        image_file_data = requests.get(imgUrl[viewNo][cutNo], headers=headers, cookies=cookies).content
    except:
        image_file_data=-1
    return image_file_data

def downImgDaemon(op, webtoonId, viewNo, cutNo, cookie):
    while True:
        td=downImg(op, webtoonId, viewNo, cutNo, cookie)
        if td==-1:
            time.sleep(0.5)
            continue
        return td

def saveImg(op, webtoonId, viewNo, cutNo, saveName, cookie):
    with open(saveName,'wb') as out:
        out.write(downImgDaemon(op, webtoonId, viewNo, cutNo, cookie))

def downPartialEpisode(op, webtoonId, start, finish, saveDir, divNo, modular, cnt, qu, savedEpisode, cookie):
    for viewNo in range(start, finish+1):
        imgNo=getImgNo(op, webtoonId, viewNo, cookie)
        for i in range(modular, imgNo, divNo):
            imgName=os.path.join(saveDir, getWebtoonName(op, webtoonId)+"_"+str(viewNo)+"_"+str(i)+".png")
            saveImg(op, webtoonId, viewNo, i, imgName, cookie)
        cnt[viewNo]-=1
        if cnt[viewNo]==0:
            qu.put(viewNo)
            log("d "+str(viewNo), 5)
    savedEpisode.value-=1

def pathChk(saveDir):
    if os.path.isdir(os.path.join(saveDir, 'tmp')):
        shutil.rmtree(os.path.join(saveDir, 'tmp'))
    os.makedirs(os.path.join(saveDir, 'tmp'))

def downWebtoon(op, webtoonId, start, finish, saveDir, mergeOption, multiThreadCount=8, multiThreadMergingCount=8, cookie=None):
    if op=='naver' or op=='nbest' or op=='nchall':
        webtoonId=int(webtoonId)
    thrs=list()
    cnt=Array('i', [multiThreadCount]*(finish+1))
    runningThreadNo=Value('i', 0)
    qu=Queue()
    leftEpisode=finish-start+1
    savedEpisode=Value('i', finish-start+1)
    for i in range(0, multiThreadCount):
        if mergeOption:
            thr = Process(target=downPartialEpisode, args=(op, webtoonId, start, finish, os.path.join(saveDir, 'tmp'), multiThreadCount, i, cnt, qu, savedEpisode, cookie))
        else:
            thr = Process(target=downPartialEpisode, args=(op, webtoonId, start, finish, saveDir, multiThreadCount, i, cnt, qu, savedEpisode, cookie))
        thrs.append(thr)
        thr.start()
    if mergeOption:
        while leftEpisode>0:
            if savedEpisode.value==0:
                multiThreadMergingCount+=multiThreadCount/2
                multiThreadCount=0
            if not qu.empty() and runningThreadNo.value<multiThreadMergingCount:
                targetEpisode=qu.get()
                if not 'imgNo' in globals() or not targetEpisode in imgNo:
                    getImgNo(op, webtoonId, targetEpisode, cookie)
                runningThreadNo.value+=1
                thr = Process(target=mergeImage, args=(op, webtoonId, targetEpisode, imgNo[targetEpisode], saveDir, runningThreadNo))
                thr.start()
                thrs.append(thr)
                leftEpisode-=1
    for i in thrs:
        i.join()

def mergeImage(op, webtoonId, viewNo, cutNo, savePath, runningThreadNo):
    file_list=[]
    size_y=[]
    ti=Image.open(os.path.join(savePath, "tmp", getWebtoonName(op, webtoonId)+"_"+str(viewNo)+"_"+str(0)+".png"))
    nx=ti.size[0]
    ti.close()
    for i in range(0, cutNo):
        file=os.path.join(savePath, "tmp", getWebtoonName(op, webtoonId)+"_"+str(viewNo)+"_"+str(i)+".png")
        image=Image.open(file)
        im=image.resize((nx, int(image.size[1]/image.size[0]*nx)))
        file_list.append(im)
        size_y.append(im.size[1])
        image.close()
    ny=sum(size_y)
    canv=Image.new("RGB", (nx, ny), (256, 256, 256))
    sumY=0
    for idx in range(len(file_list)):
        area=(0, sumY, nx, size_y[idx]+sumY)
        canv.paste(file_list[idx], area)
        sumY=sumY+size_y[idx]
    canv.save(os.path.join(savePath, getWebtoonName(op, webtoonId)+"_"+str(viewNo)+'.png'), 'PNG')
    log("m "+str(viewNo), 3)
    runningThreadNo.value-=1


if __name__=='__main__':
    freeze_support()
    pathChk(sys.argv[5])
    if len(sys.argv) - 1>8:
        if sys.argv[1]=='naver':
            cookie=NCookie(sys.argv[9], sys.argv[10])
        if sys.argv[1]=='daum':
            cookie=DCookie(sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
    else:
         cookie=None
    downWebtoon(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], (sys.argv[6]=="1"), int(sys.argv[7]), int(sys.argv[8]), cookie)
    try:
        shutil.rmtree(os.path.join(sys.argv[5], 'tmp'))
    except:
        pass