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
from contextlib import closing
import downloader

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
            print('finish spider, show result: ')
            return response.text
    except requests.RequestException:
        return None


# download image method
# def request_download(image_url,image_index):
#     r = requests.get(image_url)
#     with open(f'./image_pangzi/{image_index}.jpg', 'wb') as f:
#         f.write(r.content)   

temp_index = 0

def test_print(soup):
    # find list info from panzitv.com, according to analyse site's html
    list = soup.find(class_='imglist02 cl').find_all(class_='imgItemWrp')   

    # use global index
    global temp_index
    # to complete image url
    image_pre = 'https://www.pangzitv.com'

    for item in list:
        item_name = item.find(class_='name').string
        item_img = item.find('a').find('img').get('src')
        # use f to change int type into string
        temp_index = temp_index + 1
        print(f'Num {temp_index}' + ' | '+ item_name + ' | ' + item_img )
        # set full image url to download        
        image_url = image_pre + item_img
        # request_download(image_url, temp_index)
        # show downloader progress bar and download sth
        downloader_url(item_img, dir_url)



# downloader method
def downloader_url(download_url, dir_url):
    pass




def main(page):
    # 国产剧 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by--class--year--letter--area--lang-.html
    url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by--class--year--letter--area--lang-.html'
    html = request_url(url)
    soup = BeautifulSoup(html, 'lxml')
    test_print(soup)


def downloader_menu():
    # show downloader menu
    print('*' * 100)
    print('\t\t\t\tWelcome to use downloader!!!')
    print('Author: BestBonBai\nGithub: https://www.bestbonbai.github.io')
    print('...Crawling PangziTV...')
    print('*' * 100)




if __name__ == '__main__':
    # show downloader menu
    downloader_menu()
    
    # for i in range(0, 1):
        # main(i)


