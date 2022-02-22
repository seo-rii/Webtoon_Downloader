def makeUrl(op, webtoonId, viewNo=0):
    if op == 'naver':
        return "https://comic.naver.com/webtoon/detail.nhn?titleId=" + str(webtoonId) + "&no=" + str(viewNo)
    if op == 'nbest':
        return "https://comic.naver.com/bestChallenge/detail.nhn?titleId=" + str(webtoonId) + "&no=" + str(viewNo)
    if op == 'nchall':
        return "https://comic.naver.com/challenge/detail.nhn?titleId=" + str(webtoonId) + "&no=" + str(viewNo)
    if op == 'daum':
        return "http://webtoon.daum.net/data/pc/webtoon/viewer_images/" + str(webtoonId)
    if op == 'kakao':
        return "https://api2-page.kakao.com/api/v1/inven/get_download_data/web?productId=%s" % webtoonId


def makeRootUrl(op, webtoonId):
    if op == 'naver':
        return "https://comic.naver.com/webtoon/list.nhn?titleId=" + str(webtoonId)
    if op == 'nbest':
        return "https://comic.naver.com/bestChallenge/list.nhn?titleId=" + str(webtoonId)
    if op == 'nchall':
        return "https://comic.naver.com/challenge/list.nhn?titleId=" + str(webtoonId)
    if op == 'daum':
        return "http://webtoon.daum.net/data/pc/webtoon/view/" + str(webtoonId)
    if op == 'kakao':
        return "https://api2-page.kakao.com/api/v5/store/get/single?singleid=%s" % webtoonId
