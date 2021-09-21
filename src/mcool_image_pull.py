#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 18:02
# @Author  : Yore
# @Site    : 
# @File    : mcool_image_pull.py
# @Software: PyCharm

import requests
import os, time
from bs4 import BeautifulSoup

import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_mcool_image_pull.log'
cut_logger = get_logger(path, 'mcool_image_pull')

file_name_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'phrase': 'Top',
    'style': 'photography',
    'w': '1.0.8'
}


base_url='https://www.mcool.com/categorys-52'
if __name__ == "__main__":
    for i in range(1, 49):
        url = base_url + str(i) + '/'
        r = requests.get(url, headers=headers)
        r.encoding = 'UTF-8'
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        target_div = soup.find('div', attrs={'class': 'photo_query masonry_wrap'})
        all_items = target_div.find_all('div', attrs={'class': 'masonry_item photo_item'})
        for item in all_items:
            img_url = item.a.picture.img['data-src']
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = 'image_pull/picjumbo_image/' + str(file_name_index) + '.jpeg'
                upload_img(img_path, img_data)
                file_name_index += 1
                cut_logger.info('current file index = %s', file_name_index)
            except BaseException:
                cut_logger.info("pull error! skip current image : %s", traceback.format_exc())
        time.sleep(5)
        cut_logger.info('current file index = %s', file_name_index)
    cut_logger.info('pull done!')

