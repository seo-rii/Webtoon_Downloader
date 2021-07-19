import argparse
import os
import tempfile
from multiprocessing import Process, freeze_support, Array, Queue, Value

from tqdm import tqdm

import module.cookie as Cookie
import module.shared as shared
from module.image import getImgNo, saveImg
from module.log import log
from module.merge import mergeImage, mergeImagePdf
from module.webtooninfo import getWebtoonName


def downPartialEpisode(op, webtoonId, start, finish, saveDir, divNo, modular, cnt, qu, savedEpisode, cookie, pbar):
    for viewNo in range(start, finish + 1):
        imgNo = getImgNo(op, webtoonId, viewNo, cookie)
        for i in range(modular, imgNo, divNo):
            imgName = os.path.join(saveDir,
                                   getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png")
            saveImg(op, webtoonId, viewNo, i, imgName, cookie)
        cnt[viewNo] -= 1
        if cnt[viewNo] == 0:
            qu.put(viewNo)
            if not pbar:
                log("d " + str(viewNo), 5)
    savedEpisode.value -= 1


def pathChk(saveDir):
    try:
        os.makedirs(saveDir)
    except:
        pass


def clear():
    os.system('cls')


def downWebtoon(op, webtoonId, start, finish, saveDir, mergeOption, noProgressBar, multiThreadCount=8,
                multiThreadMergingCount=8,
                cookie=None):
    temp_dir = tempfile.TemporaryDirectory()
    pbarD = None
    pbarM = None
    if not noProgressBar:
        if mergeOption:
            pbarD = tqdm(total=finish - start + 1, maxinterval=1, position=0, desc="Download")
            pbarM = tqdm(total=finish - start + 1, maxinterval=1, position=1, desc="Merge")
        else:
            pbarD = tqdm(total=finish - start + 1, mininterval=0.01)
    if op == 'naver' or op == 'nbest' or op == 'nchall':
        webtoonId = int(webtoonId)
    thrs = list()
    cnt = Array('i', [multiThreadCount] * (finish + 1))
    runningThreadNo = Value('i', 0)
    qu = Queue()
    leftEpisode = finish - start + 1
    savedEpisode = Value('i', finish - start + 1)
    for i in range(0, multiThreadCount):
        if mergeOption:
            thr = Process(target=downPartialEpisode, args=(
                op, webtoonId, start, finish, temp_dir.name, multiThreadCount, i, cnt, qu, savedEpisode,
                cookie, not not pbarD))
        else:
            thr = Process(target=downPartialEpisode, args=(
                op, webtoonId, start, finish, saveDir, multiThreadCount, i, cnt, qu, savedEpisode, cookie,
                not not pbarD))
        thrs.append(thr)
        thr.start()
    laRunningThreadNo = 0
    if mergeOption:
        while leftEpisode > 0:
            if laRunningThreadNo != runningThreadNo.value:
                diff = laRunningThreadNo - runningThreadNo.value
                if not noProgressBar:
                    clear()
                    pbarM.update(diff)
                    clear()
                    pbarD.refresh()
                    pbarM.refresh()
                laRunningThreadNo -= diff
            if savedEpisode.value == 0 and multiThreadCount:
                multiThreadMergingCount += multiThreadCount / 2
                multiThreadCount = 0
            if not qu.empty() and runningThreadNo.value < multiThreadMergingCount:
                targetEpisode = qu.get()
                if targetEpisode not in shared.imgNo:
                    getImgNo(op, webtoonId, targetEpisode, cookie)
                if shared.imgNo[targetEpisode] == 0:
                    if not noProgressBar:
                        clear()
                        pbarM.update(1)
                        clear()
                        pbarD.refresh()
                        pbarM.refresh()
                    else:
                        log("m " + str(targetEpisode), 5)
                    leftEpisode -= 1
                    continue
                runningThreadNo.value += 1
                laRunningThreadNo += 1
                if not noProgressBar:
                    clear()
                    pbarD.update(1)
                    clear()
                    pbarD.refresh()
                    pbarM.refresh()
                if mergeOption == 1:
                    thr = Process(target=mergeImage, args=(
                        op, webtoonId, targetEpisode, shared.imgNo[targetEpisode], saveDir, temp_dir.name,
                        runningThreadNo, cookie, len(str(finish))))
                else:
                    thr = Process(target=mergeImagePdf, args=(
                        op, webtoonId, targetEpisode, shared.imgNo[targetEpisode], saveDir, temp_dir.name,
                        runningThreadNo, cookie, noProgressBar, len(str(finish))))
                thr.start()
                thrs.append(thr)
                leftEpisode -= 1
    for i in thrs:
        i.join()
    temp_dir.cleanup()
    if not noProgressBar:
        diff = laRunningThreadNo - runningThreadNo.value
        if not noProgressBar:
            clear()
            pbarM.update(diff)
            clear()
            pbarD.refresh()
            pbarM.refresh()
        laRunningThreadNo -= diff
        clear()
        pbarD.close()
        pbarM.close()


if __name__ == '__main__':
    freeze_support()
    parser = argparse.ArgumentParser(description='Webtoon Downloader 3.4.0',
                                     epilog="Copyright 2019-2020 Seohuyun Lee. " +
                                            "This program is distributed under MIT license. " +
                                            "Visit https://github.com/Seo-Rii/Webtoon_Downloader to get more information.")
    parser.add_argument('Type', type=str,
                        help='Webtoon provider. One of naver, nbest, nchall, daum, and kakao.',
                        choices=['naver', 'nbest', 'nchall', 'daum', 'kakao'])
    parser.add_argument('ID', type=str, help='Webtoon ID.')
    parser.add_argument("-s", "--start", type=int, required=True, help='Episode Number to Start download.')
    parser.add_argument("-f", "--finish", type=int, required=True, help='Episode Number to Finish download.')
    parser.add_argument("--downThreadNo", type=int, default=4, help='Thread Number to download Webtoon.')
    parser.add_argument("--mergeThreadNo", type=int, default=4, help='Thread Number to merge Webtoon.')
    merge = parser.add_mutually_exclusive_group()
    merge.add_argument("--mergeAsPng", help='Thread Number to merge Webtoon.', action='store_true')
    merge.add_argument("--mergeAsPdf", help='Thread Number to merge Webtoon.', action='store_true')
    parser.add_argument("--noProgressBar", help='Do not beautify progress with tqdm.', action='store_true')
    parser.add_argument('Path', type=str, help='Path to save Webtoon.')
    parser.add_argument('cookie', type=str, nargs='*',
                        help='Cookie value to authorize while downloading Webtoon. Find document to get info.')
    args = parser.parse_args()
    pathChk(args.Path)
    cookie = None
    try:
        if args.Type == 'naver' or args.Type == 'nbest' or args.Type == 'nchall':
            cookie = Cookie.NCookie(args.cookie[0], args.cookie[1])
        if args.Type == 'daum':
            cookie = Cookie.DCookie(args.cookie[0], args.cookie[1], args.cookie[2], args.cookie[3], args.cookie[4])
        if args.Type == 'kakao':
            cookie = Cookie.KCookie(args.cookie[0], args.cookie[1], args.cookie[2], args.cookie[3], args.cookie[4])
    except:
        pass

    mergeOption = 0
    if args.mergeAsPng:
        mergeOption = 1
    if args.mergeAsPdf:
        mergeOption = 2

    downWebtoon(args.Type, args.ID, args.start, args.finish, args.Path, mergeOption, args.noProgressBar,
                args.downThreadNo, args.mergeThreadNo, cookie)
