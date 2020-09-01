# Webtoon_Downloader

<img alt="logo" src="./logo.png" width="100">  
  
[![Build Status](https://travis-ci.com/Seo-Rii/Webtoon_Downloader.svg?branch=master)](https://travis-ci.com/Seo-Rii/Webtoon_Downloader)  
  
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
