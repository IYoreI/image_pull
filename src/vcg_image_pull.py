#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/21 10:56
# @Author  : Yore
# @Site    : 
# @File    : vcg_image_pull.py
# @Software: PyCharm


import requests
import os, time
from bs4 import BeautifulSoup
import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_vcg_image_pull.log'
cut_logger = get_logger(path, 'vcg_image_pull')

file_name_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
request_params = {
    'transform': 'chengshi'
}
base_url = 'https://www.vcg.com/creative-image/chengshi/'

if __name__ == "__main__":
    for i in range(1, 200):
        request_params['page'] = str(i)
        r = requests.get(url=base_url, headers=headers, params=request_params)
        text = r.content
        soup = BeautifulSoup(text, 'html.parser')

        target_div = soup.find('div', attrs={'class': 'gallery_inner'})
        all_items = target_div.find_all('figure', attrs={'class': 'galleryItem'})
        for item in all_items:
            img_url = 'http:' + item.a.img['data-min']
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = '../image/vcg_image/' + str(file_name_index) + '.jpeg'
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)

            except BaseException:
                cut_logger.info("splitshire pull error! skip current image : %s", traceback.format_exc())
            cut_logger.info('splitshire 当前爬取页面下标：%s,爬取总图片数：%s', i, file_name_index)
            file_name_index += 1
    cut_logger.info('splitshire pull done! current file index:%s', file_name_index)
