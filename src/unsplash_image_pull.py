#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 8:59
# @Author  : Yore
# @Site    :
# @File    : unsplash_image_pull.py
# @Software: PyCharm


import requests
import os, time

import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_unsplash_image_pull.log'
cut_logger = get_logger(path, 'unsplash_image_pull')

file_name_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'xp-landing-pages-aggressive-affiliates-v1=experiment; xp-search-aggressive-affiliates-v1=control; xp-video-direct-ads-topics=disabled; ugid=593e7ad86de17573ed36c40ead6b6c085440340; _ga=GA1.2.2068867874.1632102179; _gid=GA1.2.485083806.1632102179; _sp_ses.0295=*; lux_uid=163210217919166449; uuid=1639b0d0-19b4-11ec-a93a-1d4f227048fd; xpos={}; azk=1639b0d0-19b4-11ec-a93a-1d4f227048fd; azk-ss=true; _sp_id.0295=d8445cbc-c436-4f74-a312-2900714def57.1632102179.1.1632102241.1632102179.6a239be8-db8a-46c7-a361-2a27b98cb131',
    'Connection': 'keep-alive'
}
request_params = {
    'per_page': '12'
}
base_url = 'https://unsplash.com/napi/photos'

if __name__ == "__main__":
    for i in range(1, 5000):
        request_params['page'] = str(i)
        r = requests.get(url=base_url, headers=headers, params=request_params)
        r.encoding = 'UTF-8'
        info_list = r.json()

        for item in info_list:
            img_url = item['urls']['full']
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = '../image/unsplash_image/' + str(file_name_index) + '.jpeg'
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)

            except BaseException:
                cut_logger.info(" unsplash  pull error! skip current image : %s", traceback.format_exc())
            cut_logger.info('unsplash 当前爬取页面下标：%s,爬取总图片数：%s', i, file_name_index)
            file_name_index += 1
    cut_logger.info('unsplash  pull done!')
