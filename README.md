# Webtoon_Downloader

<img alt="logo" src="./logo.png" width="100" height="100">  
  
[![Build Status](https://travis-ci.org/04SeoHyun/Webtoon_Downloader.svg?branch=master)](https://travis-ci.org/04SeoHyun/Webtoon_Downloader)  
  
Webtoon Downloader made with Python3

## Download

[Webtoon_Doanloader 2.2.1](https://github.com/04SeoHyun/Webtoon_Downloader/releases/tag/2.2.1)

## Supported sites

Naver
- Supported types
    - Naver Webtoon(정식연재)
    - Best Challenge(베스트 도전)
    - Challenge(도전만화)
- Supported Function
    - Authorize Adult with Cookies

Daum
- Supported types
    - Daum Webtoon
- Supported Function
    - Authorize Adult with Cookies
    - Authorize non-free webtoon with Cookies

## Usage

webtoon-download.exe op, webtoonId, start, finish, saveDir, mergeOption, multiThreadCount, multiThreadMergingCount [, Cookie]

- op  
naver, nbest, nchall, daum, kakao
- webtoonId  
Webtoon ID
    - naver, nbest, nchall
    6-digit number on webtoon URL
    - daum, kakao
    Specific string on webtoon URL
- start  
Start Episode No
- finish  
End Episode No
- saveDir  
Path to Save Results
- mergeOption  
    - 0.Do not Merge
    - 1.Merge as Long PNG
    - 2.Merge as PDF
- multiThreadCount  
Maximum Count of Downloader Thread
- multiThreadMergingCount  
Maximum Count of Merger Thread
- Cookie  
This parameter is Optional.  
Important! Split with Space
    - naver, nbest, nchall
    NID_AUT, NID_SES
    - daum
    HM_CU, HTS, PROF, TS, LSID