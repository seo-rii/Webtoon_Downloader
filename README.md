# Webtoon_Downloader

<img alt="logo" src="./logo.png" width="100">  
  
[![Build Status](https://travis-ci.com/Seo-Rii/Webtoon_Downloader.svg?branch=master)](https://travis-ci.com/Seo-Rii/Webtoon_Downloader) 

**English descryption is below.**  

파이썬으로 만든 멀티프로세스 활용 웹툰 다운로더입니다!

## 다운받기
 
[Seo-Rii/Webtoon_Downloader_UI](https://github.com/Seo-Rii/Webtoon_Downloader_UI)  

## 특징
- 멀티프로세스 활용
- 다양한 저장 옵션(pdf, 이미지 하나로, ...)
- 인증이 필요한 웹툰(유료, 성인) 지원
- 다양한 플랫폼 지원

### 현재 지원중인 곳

네이버 웹툰
- 베스트 도전, 도전만화도 지원해요!
- 쿠키값으로 성인인증이 가능합니다.

다음 웹툰
- 쿠키값으로 성인인증/구매한 작품 다운이 가능합니다.

카카오 페이지

### 개발중

네이버 웹툰
 - 스크롤툰(스크롤시 효과가 있는 웹툰. ex)가담항설, 모태솔로수용소, ...)

카카오페이지
- 쿠키로 계정 인증

Webtoon(라인 웹툰)

## 사용법

Webtoon_Downloader.py [-h] -s START -f FINISH [--downThreadNo DOWNTHREADNO] [--mergeThreadNo MERGETHREADNO] [--mergeAsPng | --mergeAsPdf] [--noProgressBar]  {naver,nbest,nchall,daum,kakao} ID Path [cookie [cookie ...]]


필수 옵션:  
- {naver,nbest,nchall,daum,kakao,webtoon}   
    웹툰 플랫폼  
    - naver : 네이버 웹툰
    - nbest : 네이버 베도
    - nchall : 네이버 도전만화
    - daum : 다음 웹툰
    - kakao : 카카오페이지
    - webtoon : 라인 웹툰
- ID  
    웹툰 아이디(일련번호)  
    웹툰 링크 뒤에 있는 숫자/영어
- Path  
    Path to save Webtoon.  
- cookie  
    Cookie value to authorize while downloading Webtoon.
    - naver, nbest, nchall  
    NID_AUT, NID_SES
    - daum  
    HM_CU, HTS, PROF, TS, LSID
    - kakao  
    HM_CU, HTS, PROF, TS, LSID, _kawIp, _kawIptea, _kawIt, _kawItea

선택 옵션:
- -h, --help  
    show this help message and exit
- -s START, --start START  
    Episode Number to Start download.
- -f FINISH, --finish FINISH  
    Episode Number to Finish download.
- --downThreadNo DOWNTHREADNO  
    Thread Number to download Webtoon.  
    Default value is 4.  
- --mergeThreadNo MERGETHREADNO  
    Thread Number to merge Webtoon.  
    Default value is 4.  
    
- --mergeAsPng  
    Merge Webtoon images into Long PNG File.  
- --mergeAsPdf  
    Merge Webtoon images into PDF File.  
- --noProgressBar  
    Do not beautify progress with tqdm.

#English 
  
Webtoon Downloader made with Python3

## Download

[Webtoon_Doanloader 3.4.0](https://github.com/04SeoHyun/Webtoon_Downloader/releases/tag/3.4.0)

## Features

- Multi-processed
- Various merging options
- Supports authorization with cookie
- Supports various sites(see below)

### Supported sites

Naver Webtoon
- Supported types
    - Naver Webtoon(정식연재)
    - Best Challenge(베스트 도전)
    - Challenge(도전만화)
    - Common webtoon
    - Cuttoons
- Supported Function
    - Authorize Adult with Cookies

Daum Webtoon
- Supported types
    - Daum Webtoon
- Supported Function
    - Authorize Adult with Cookies
    - Authorize non-free webtoon with Cookies

Kakao Pages(Beta)
- Supported types
    - Kakao Pages Webtoon

### Coming Soon

Naver Webtoon
 - Supported types
    - Scroll toon(effect while scrolling)

Kakao Pages
- Supported Function
    - Authorize non-free webtoon with Cookies

Webtoon(Webtoons.com)
- Supported types
    - Official Webtoon(Weekly Uploaded)
    - Canvas(Challenge)

## Usage

Webtoon_Downloader.py [-h] -s START -f FINISH [--downThreadNo DOWNTHREADNO] [--mergeThreadNo MERGETHREADNO] [--mergeAsPng | --mergeAsPdf] [--noProgressBar]  {naver,nbest,nchall,daum,kakao} ID Path [cookie [cookie ...]]


positional arguments:  
- {naver,nbest,nchall,daum,kakao,webtoon}   
    Webtoon provider.  
    - naver : Naver Webtoon
    - nbest : Naver Best Challange
    - nchall : Naver Challange
    - daum : Daum Webtoon
    - kakao : Kakao Pages
    - webtoon : Webtoons.com
- ID  
    Webtoon ID.  
    - naver, nbest, nchall  
    6-digit number on webtoon URL
    - daum, kakao  
    Specific string on webtoon URL
- Path  
    Path to save Webtoon.  
- cookie  
    Cookie value to authorize while downloading Webtoon.
    - naver, nbest, nchall  
    NID_AUT, NID_SES
    - daum  
    HM_CU, HTS, PROF, TS, LSID
    - kakao  
    HM_CU, HTS, PROF, TS, LSID, _kawIp, _kawIptea, _kawIt, _kawItea

optional arguments:
- -h, --help  
    show this help message and exit
- -s START, --start START  
    Episode Number to Start download.
- -f FINISH, --finish FINISH  
    Episode Number to Finish download.
- --downThreadNo DOWNTHREADNO  
    Thread Number to download Webtoon.  
    Default value is 4.  
- --mergeThreadNo MERGETHREADNO  
    Thread Number to merge Webtoon.  
    Default value is 4.  
    
- --mergeAsPng  
    Merge Webtoon images into Long PNG File.  
- --mergeAsPdf  
    Merge Webtoon images into PDF File.  
- --noProgressBar  
    Do not beautify progress with tqdm.
