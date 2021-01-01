# This project is to crawl info from pangzitv.com, such as movies...

import requests
from bs4 import BeautifulSoup
import xlwt
import os
# create a new dir to store images
os.makedirs('./image_pangzi/', exist_ok=True)


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
def request_download(image_url,image_index):
    r = requests.get(image_url)
    with open(f'./image_pangzi/{image_index}.jpg', 'wb') as f:
        f.write(r.content)   


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

                   




def main(page):
    # 国产剧 https://www.pangzitv.com/vod-list-id-12-pg-1-order--by--class--year--letter--area--lang-.html
    url = 'https://www.pangzitv.com/vod-list-id-12-pg-' + str(page) + '-order--by--class--year--letter--area--lang-.html'
    html = request_url(url)
    soup = BeautifulSoup(html, 'lxml')
    
    test_print(soup)


if __name__ == '__main__':
    print('crawling PangziTV: ')
    for i in range(0, 1):
        main(i)


