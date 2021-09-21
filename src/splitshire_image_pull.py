#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/18 10:38
# @Author  : Yore
# @Site    : 
# @File    : splitshire_image_pull.py
# @Software: PyCharm

import requests
import os, time
from bs4 import BeautifulSoup

import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_split_image_pull.log'
cut_logger = get_logger(path, 'split_image_pull')

file_name_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
request_param = {}
base_url = 'https://www.splitshire.com/best-new-free-stock-photos/'

if __name__ == "__main__":
    for i in range(1, 42):
        url = base_url
        request_param['_page'] = str(i)

        r = requests.get(url, headers=headers, params=request_param)
        r.encoding = 'utf-8'
        text = r.content
        soup = BeautifulSoup(text, 'html.parser')

        target_div = soup.find('div', attrs={
            'class': 'pt-cv-view pt-cv-pinterest pt-cv-colsys pt-cv-border pt-cv-no-bb pt-cv-pgregular pt-cv-center'})
        all_items = target_div.find_all('div', attrs={'class': 'pt-cv-pinmas'})
        for item in all_items:
            img_url = item.a.img['src']
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = '../image/split_image/' + str(file_name_index) + '.jpeg'
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)

            except BaseException:
                cut_logger.info("splitshire pull error! skip current image : %s", traceback.format_exc())
            cut_logger.info('splitshire 当前爬取页面下标：%s,爬取总图片数：%s', i, file_name_index)
            file_name_index += 1
    cut_logger.info('splitshire pull done! current file index:%s', file_name_index)
