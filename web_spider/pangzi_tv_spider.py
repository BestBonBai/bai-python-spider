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



# create a new dir to store images
dir_url = './image_panzi/'
os.makedirs(f'{dir_url}', exist_ok=True)


def request_url(url):
    headers = {
    # 假装自己是浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    try:
        response = requests.get(url,headers=headers)
        # status 200 means connected success
        if response.status_code == 200:
            print('showing result: ')
            return response.text
    except requests.RequestException:
        return None


# download image method
# def request_download(image_url,image_index):
#     r = requests.get(image_url)
#     with open(f'./image_pangzi/{image_index}.jpg', 'wb') as f:
#         f.write(r.content)   

temp_index = 0
CHECK_REGX = '^http' # check correct regex expression

def test_print(soup):
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
        downloader_url(temp_index, image_url, item_img_url, item_name, dir_url, movie_link)



# save info in txt file
def save_info_txt(temp_index, item_name, location_url, movie_link):
    my_file_name = 'my_info_file.md'
    # add info in the back of the file, if not exist, create new file
    my_info_file = open(my_file_name, 'a')
    total_info = '### ' + str(temp_index) + ': [' + item_name + '](' + movie_link +')\n' + '![](' + location_url + ')\n'
    my_info_file.write(total_info)
    my_info_file.close()


# downloader method
def downloader_url(temp_index, image_url, item_img_url, item_name, dir_url, movie_link):
    
    download_url = image_url
    filename = item_img_url.split('/')[-1]
    
    # save images
    my_location = f'{dir_url}/{filename}'
    # save info in text
    location_url = f'{dir_url}/{filename}' # need to change for markdown image is this format
    save_info_txt(temp_index, item_name, location_url, movie_link)

    # such image files (no txt file) use b to binary store
    r = requests.get(download_url)
    with open(my_location, 'wb') as f:
        f.write(r.content)     




def main(page, type):
    # 国产剧 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by--class--year--letter--area--lang-.html
    # 热门点击 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by-hits-class-0-year-0-letter--area--lang-.html
    if(type == '0'):
        url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by--class--year--letter--area--lang-.html'
        print('国产剧 download...')
    if(type == '1'):
        url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by-hits-class-0-year-0-letter--area--lang-.html'
        print('热播剧 download...')
    html = request_url(url)
    soup = BeautifulSoup(html, 'lxml')
    test_print(soup)


def downloader_menu():
    # show downloader menu
    print('*' * 100)
    print('\t\t\t\tWelcome to use Spider!!!')
    print('Author: BestBonBai\nGithub: https://www.bestbonbai.github.io')
    print('...Crawling PangziTV...')
    print('*' * 100)
    type = input('Please choose type to download:\n 0: 国产剧, 1: 热门点击\n')
    return type




if __name__ == '__main__':
    # show downloader menu
    type = downloader_menu()
    # main(1,type)
    for i in range(0, 1):
        main(i,type)


