# Web spider
The project is to learn how to crawl info by python
## Projects
- [x] douban top movies list spider
    - [ ] doing some different saving function
- [ ] panzi top movies download
- [ ] downloader : a smart download tool to show progess
## Install instruction for Mac
- using code `sudo python3 -m` before pip codes to install requests lib in python 3 instead of default python 2 in Mac
```python
sudo python3 -m pip install requests
sudo python3 -m pip install beautifulsoup4
sudo python3 -m pip install lxml
```
## Don't forget to fake headers
```python
headers = {
        # 假装自己是浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    try:
        response = requests.get(url,headers=headers)
```
