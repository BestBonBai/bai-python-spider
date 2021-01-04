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
- [x] 9. add `progress bar` method to show download status

## running instruction
- make sure `pangzi_tv_spider_v2.py` in correct dir
- run `pangzi_tv_spider_v2.py`
- **Don't interrupt** it when running, it will automatic create specified dir and files.

show some codes below:
```bash
# some cmd to run spider
python3 pangzi_tv_spider_v2.py
# following the interactive code 

```

- if download, please make sure input valid url

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


### Some codes about extract and download all '.ts' files, merge them, and delete them
```python
# implement download m3u8 files
def get_m3u8_url_decode(soup_my_url):
    # find unescape url, use regex to find
    list = soup_my_url.find(class_='clear pl-play js-addDanmu').find_all('script')
    # print(list[0])
    m3u8_file_name = soup_my_url.find('h3').string
    print('File name: ' + m3u8_file_name)
    # create a dir
    os.makedirs(f'{dir_download_url}/{m3u8_file_name}', exist_ok=True)
    file_path = f'{dir_download_url}/{m3u8_file_name}'
    print('[Create a new dir success!]')
    # spilt the encoded mac_url, list[0] is not a string type, re.findall returns a list
    encode_url = re.findall(r'unescape\(base64decode\(.+\'', str(list[0]), re.M | re.VERBOSE | re.DOTALL)
    # print(encode_url[0])
    # 1. split unescape(base64decode(, get mac_url including '' quote
    split_encode_url = encode_url[0].split('unescape(base64decode(')[-1]
    # print(split_encode_url)
    # 2. decode base64, then 3. unescape this url
    decode_base64_url = base64.b64decode(split_encode_url)
    # print(decode_base64_url)
    unescape_url = parse.unquote(str(decode_base64_url))
    # print(unescape_url)
    # 4. need split again '#part 2$'
    # real_url = unescape_url.split('#')
    # print(real_url)
    # 5. use list to get all url
    all_parts_list = []
    # for part_url in real_url:
        # add all elements into list
        # all_parts_list.append(part_url.split('$')[-1])
    # update 5: find all valid http url
    all_parts_list = re.findall(r'(https:.*\.m3u8)', str(unescape_url), re.M)
    print('[Debug] Download File parts: ')
    print(all_parts_list)

    # get all ts files of m3u8
    for i in range(len(all_parts_list)):
        all_parts_info = all_parts_list[i]
        get_ts_files(all_parts_list[i], i, file_path)
    # get_ts_files(all_parts_list[0], 0, file_path)



def get_ts_files(parts_info, i, file_path):
    # create a dir
    os.makedirs(f'{file_path}/{i}', exist_ok=True)
    # find all info from m3u8_url

    # test_url = 'https://cdn9.pztv.ca/upload/20210101/d6dfa215e40c638bfa04beae6d037adc/d6dfa215e40c638bfa04beae6d037adc.m3u8'
    test_url = parts_info
    print(test_url)
    # get content of test_url
    all_content = request_url(test_url)
    # print(all_content)   
    # for line in file_line:
        # print(line)
    # write a m3u8 file
    with open(f'{file_path}/{i}/part{i}.m3u8', 'w') as f:
        f.write(all_content)
        print('[success download m3u8]')

    # get each ts url
    # read each line
    tslist = []
    test_main_url = test_url
    print('[Test Url]: ' + test_main_url)
    file_line = all_content.split('\n')
    for line in file_line:
        if re.match('[^#]', line):
            # use regex to replace the last '/' content
            # print(line)
            # re.sub return a str
            new_test_url = re.sub(r'[^\/]+(?!.*\/)', f'{line}', test_main_url)
            # print(new_test_url)
            tslist.append(f'{new_test_url}')
            # print(line[-6:]) # get string from end, has bug for diff length of xxx.ts, xxxx.ts
    # print(tslist)
    print('[Num tslist]: ' + str(len(tslist)))
    # ask if it starts downloading
    ask_start = input('Would you like to download now? (y/n): \n')
    if ask_start == 'y':
        # download each ts file
        download_ts_files(tslist, file_path, i)
    else:
        # no download
        print('you can download later...')
        sys.exit(0)



# download each ts file
def download_ts_files(tslist, file_path, i):
    for item_ts in tslist:
        ts_name = item_ts.split('/')[-1]
        # download file path
        ts_file_path = f'{file_path}/{i}/{ts_name}'
        # call request content method
        print('[Prepare File Name]: ' + f'{ts_name}')
        request_url_content(item_ts, ts_file_path)
        # print('[downloaded]' + f'{ts_name}')
        # create new file
        # with open(f'{file_path}/{i}/{ts_name}', 'ab') as f:
        #     f.write(ts_content)
        #     print('[success download]' + f'{ts_name}')
    # when finish, ask if start merge ts file
    is_merge = input('Downloaded all ts files, start merge now? (y/n)\n')
    if is_merge == 'y':
        # call merge method
        merge_file_name = f'part{i}'
        new_file_path = f'{file_path}/{i}/'
        merge_ts(new_file_path, merge_file_name)
    else:
        print('Finished, you can use merge_ts.py to merge them later!\n')
        sys.exit(0)


# merge ts file method
def merge_ts(new_file_path, merge_file_name):
    """
        use cmd to merge file
    """
    tsPath = new_file_path

    #获取所有的ts文件
    path_list = os.listdir(f'{tsPath}')
    #对文件进行排序并将排序后的ts文件路径放入列表中
    path_list.sort()
    li = [os.path.join(tsPath,filename) for filename in path_list if '.ts' in filename]
    #将ts路径并合成一个字符参数
    tsfiles = '|'.join(li)

    # print(tsfiles)

    #指定输出文件名称
    saveMp4file = tsPath + f'{merge_file_name}.mp4'

    #调取系统命令使用ffmpeg将ts合成mp4文件
    cmd = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s'% (tsfiles,saveMp4file)
    os.system(cmd)
    # check if delete ts files
    delete_file = input('Would you like to delete all ts files? (y/n): \n')
    if delete_file == 'y':
        remove_ts(tsPath)
    else:
        print('you can delete later......')
        sys.exit(0)




def remove_ts(tsPath):
    for inline in glob.glob(os.path.join(tsPath, '*.ts')):
        os.remove(inline)
    print('finish delete ts files!')


```
