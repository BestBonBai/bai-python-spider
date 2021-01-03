# Web spider
The project is to learn how to crawl info by python
## Projects
- [x] douban top movies list spider
    - [ ] doing some different saving function
- [ ] panzi top movies download
    - [x] finish download image and link and movies list
    - [x] create a markdown file to show the movies list and links
    - [x] save images of movies
    - [x] trying to download movies
        - [x] [spider version 2](/pangzi_tv_spider_v2.py)
- [ ] downloader : a smart download tool to show progess

## Install instruction for Mac
- using code `sudo python3 -m` before pip codes to install requests lib in python 3 instead of default python 2 in Mac
```python
sudo python3 -m pip install requests
sudo python3 -m pip install beautifulsoup4
sudo python3 -m pip install lxml
```
- **Attention**: 
    - [x] some files need to set privilege of read & write for specific user!!! 
    - [x] some **bugs** are `tab & space` issues in vscode
## Don't forget to fake headers
```python
headers = {
        # 假装自己是浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    try:
        response = requests.get(url,headers=headers)
```

## Some technical issues solved
- [x] 1. Get m3u8 encode link
- [x] 2. decode by `base64decode` and `urllib->parse.unquote(str)`
- [x] 3. more practice `Regex` expression
    - [x] use `split` and `regex` to get valid `filename` and `url`
- [x] write **non-txt** file by `ab` which `b` means `binary`
- [x] 4. `debug` correct store path
- [x] 5. download all `*.ts` file
- [x] 6. `MacOs` : use `ffmpeg` to `merge` all `*.ts` files to `.mp4` file
    - `ffmpeg` use `brew install ffmpeg`
- [x] 7. delete all `.ts` files after `merge` done
- [x] 8. `fix` some `bugs` during running time

## Import all packages by python
```python
import requests
from bs4 import BeautifulSoup
import xlwt # for execl file
import os
# import my class
import sys
# sys.path.append('需要作为模块引入的路径')
# sys.path.append("./")
import re # for regex
import base64 # for base64decode
# import html # for unescape
import time
import glob
from urllib import parse
```
