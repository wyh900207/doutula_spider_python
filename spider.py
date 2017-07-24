# -*- encoding: utf-8 -*-

import requests
import urllib
import os
import threading
from bs4 import BeautifulSoup

BASE_URL = 'https://www.doutula.com/photo/list/?page='
page_url_list = []
image_url_list = []
gLock = threading.Lock()


for page_index in range(1, 2):
    url = BASE_URL + str(page_index)
    page_url_list.append(url)


def produce():
    current_index = 0
    while current_index < 2:
        gLock.acquire()
        if len(page_url_list) is 0:
            gLock.release()
            break
        else:
            current_index += 1
            page_url = page_url_list.pop()
            gLock.release()
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'lxml')
            page_image_url_list = soup.find_all('img', attrs={'class':
                                                              'img-responsive lazy image_dta'})
            gLock.acquire()
            for img in page_image_url_list:
                url = img['data-original']
                if not url.startswith('http'):
                    url = 'https:' + url
                image_url_list.append(url)
            gLock.release()


def customer():
    current_index = 0
    while current_index < 2:
        gLock.acquire()
        if len(image_url_list) is 0:
            gLock.release()
            continue
        else:
            image_url = image_url_list.pop()
            gLock.release()
            image_name = image_url.split('/').pop()
            image_path = os.path.join('doutula_images', image_name)
            urllib.urlretrieve(image_url, filename=image_path)


def main():
    for x in range(3):
        thread = threading.Thread(target=produce)
        thread.start()
    for x in range(3):
        thread = threading.Thread(target=customer)
        thread.start()


if __name__ == '__main__':
    main()
