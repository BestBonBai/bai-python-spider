#-*- coding: UTF-8 -*-
# This project is to crawl info from pangzitv.com, such as movies...

import requests
from bs4 import BeautifulSoup
import xlwt
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

requests.packages.urllib3.disable_warnings()  # close https verify

# create a new dir to store images
dir_url = './image_pangzi/'
os.makedirs(f'{dir_url}', exist_ok=True)
# create new download dir
dir_download_url = './download_pangzi/'
os.makedirs(f'{dir_download_url}', exist_ok=True)

# get response.text for html
def request_url(url):
    headers = {
    # 假装自己是浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    try:
        response = requests.get(url,headers=headers, verify=False)
        # status 200 means connected success
        if response.status_code == 200:
            print('showing result: ')
            # print(response.text)
            return response.text
    except requests.RequestException:
        return None

# get response.content
def request_url_content(url, ts_file_path):
    headers = {
    # 假装自己是浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    # add progress bar
    start = time.time() #下载开始时间
    # response = requests.get(url, stream=True)
    size = 0    #初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小   

    try:
        response = requests.get(url,headers=headers, verify=False, stream=True)
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        # status 200 means connected success
        if response.status_code == 200:
            # print('showing result: ')
            # print(response.text)
            # add progress bar
            print('Start download,[File size]:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   #开始下载，显示下载文件大小
            filepath = ts_file_path  # set file path
            # create new file
            with open(f'{filepath}','ab') as file:   #显示进度条
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+'[download progess]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
            end = time.time()   # end time
            print('Download completed!,times: %.2fs' % (end - start))  # print end time

            # return response.content
    except requests.RequestException:
        print('[DOWNLOAD ERROR]')
        return None

# download image method
# def request_download(image_url,image_index):
#     r = requests.get(image_url)
#     with open(f'./image_pangzi/{image_index}.jpg', 'wb') as f:
#         f.write(r.content)

temp_index = 0
CHECK_REGX = '^http' # check correct regex expression

def test_print(soup, type):
    # find list info from panzitv.com, according to analyse site's html
    list = soup.find(class_='imglist02 cl').find_all(class_='imgItemWrp')

    # use global index
    global temp_index
    # to complete image url
    image_pre = 'https://www.pangzitv.com'

    for item in list:
        item_name = item.find(class_='name').string
        item_img_url = item.find('a').find('img').get('src')
        item_link = item.find(class_='name').get('href')
        # use f to change int type into string
        temp_index = temp_index + 1
        print(f'Num {temp_index}' + ' | '+ item_name + ' | ' + item_img_url + ' | ' + item_link )
        # regex check
        match_url = re.match(r'^http', item_img_url, re.I)
        if(match_url):
            image_url = item_img_url
        else:
            # set full image url to download
            image_url = image_pre + item_img_url
        movie_link = image_pre + item_link

        # request_download(image_url, temp_index)
        # show downloader progress bar and download sth
        downloader_url(temp_index, image_url, item_img_url, item_name, dir_url, movie_link, type)



# save info in txt file
def save_info_txt(temp_index, item_name, location_url, movie_link, type):
    if(type == '0'):
        my_file_name = 'my_info_guochan_tv.md'
    elif(type == '1'):
        my_file_name = 'my_info_hot_tv.md'
    elif(type == '2'):
        my_file_name = 'my_info_new_movies.md'
    else:
        print('incorrect type!')
    # my_file_name = 'my_info_file.md'
    # add info in the back of the file, if not exist, create new file
    my_info_file = open(my_file_name, 'a')
    total_info = '### ' + str(temp_index) + ': [' + item_name + '](' + movie_link +')\n' + '![](' + location_url + ')\n'
    my_info_file.write(total_info)
    my_info_file.close()


# downloader method
def downloader_url(temp_index, image_url, item_img_url, item_name, dir_url, movie_link, type):

    download_url = image_url
    filename = item_img_url.split('/')[-1]

    # save images
    my_location = f'{dir_url}/{filename}'
    # save info in text
    location_url = f'{dir_url}/{filename}' # need to change for markdown image is this format
    save_info_txt(temp_index, item_name, location_url, movie_link, type)

    # such image files (no txt file) use b to binary store
    r = requests.get(download_url)
    with open(my_location, 'wb') as f:
        f.write(r.content)




def main(page, type):
    # 国产剧 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by--class--year--letter--area--lang-.html
    # 热门点击 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by-hits-class-0-year-0-letter--area--lang-.html
    # 最新电影 https://www.pangzitv.com/vod-type-id-1-pg-1.html
    if(type == '0'):
        url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by--class--year--letter--area--lang-.html'
        print('国产剧 download...')
    elif(type == '1'):
        url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by-hits-class-0-year-0-letter--area--lang-.html'
        print('热播剧 download...')
    elif(type == '2'):
        url = 'https://www.pangzitv.com/vod-type-id-1-pg-' + str(page) + '.html'
        print('最新电影 download...')
    elif(type == '3'):
        # my_url = input('Please enter an url to download movies or tv\n')
        # test download m3u8 method
        # my_url = 'https://www.pangzitv.com/vod-play-id-82719-src-1-num-1.html'
        my_url = input('Please enter a valid url to download movies:\n')
        # regex check
        check_my_url = re.match(r'^https://www.pangzitv.com/', my_url, re.I)
        print('File download...')   
    else:
        print('incorrect input!!!')

    if(type == '3'): 
        if(check_my_url):
            html = request_url(my_url)
            # print(html)
            soup_my_url = BeautifulSoup(html, 'lxml')
            # get m3u8 url
            get_m3u8_url_decode(soup_my_url)
        else:
            print('incorrect url!!!')
    else:   
        html = request_url(url)
        soup = BeautifulSoup(html, 'lxml')
        # paragm: type to create my_file_name
        test_print(soup, type)



def downloader_menu():
    # show downloader menu
    print('*' * 100)
    print('\t\t\t\tWelcome to use Spider!!!')
    print('Author: BestBonBai\nGithub: https://www.bestbonbai.github.io')
    print('...Crawling PangziTV...')
    print('*' * 100)
    type = input('Please choose type to download:\n 0: 国产剧, 1: 热门点击, 2: 最新电影, 3: Download， 9: Exit\n')
    return type


# implement download m3u8 files
def get_m3u8_url_decode(soup_my_url):
    # find unescape url, use regex to find
    list = soup_my_url.find(class_='clear pl-play js-addDanmu').find_all('script')
    # print(list[0])
    m3u8_file_name = soup_my_url.find('h3').string
    # fix bug, replace all space (such as xxx ddd to xxx-ddd) by '-'
    m3u8_file_name = re.sub(r'\s', '-', m3u8_file_name)
    print('M3U8 File name: ' + m3u8_file_name)
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



if __name__ == '__main__':
    # show downloader menu
    type = downloader_menu()
    # choose how mang pages need to crawl
    if type == '9':
        print('Exit')
    else:    
        numPage = input('Please enter page amounts: (if you want download, input 1)\n')
        for i in range(0, int(numPage)):
            main(i,type)
