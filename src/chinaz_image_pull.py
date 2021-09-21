#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/17 15:59
# @Author  : Yore
# @Site    : 
# @File    : chinaz_image_pull.py
# @Software: PyCharm


import requests
import os, time
from bs4 import BeautifulSoup

import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_chinaz_image_pull.log'
cut_logger = get_logger(path, 'chinaz_image_pull')

file_name_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'qHistory=aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy9pbWd0b2Jhc2UvX2Jhc2U2NOWbvueJh+WcqOe6v+i9rOaNouW3peWFtw==; Hm_lvt_398913ed58c9e7dfe9695953fb7b6799=1631865466; Hm_lpvt_398913ed58c9e7dfe9695953fb7b6799=1631865691',
    'Connection': 'keep-alive',
    'phrase': 'Top',
    'style': 'photography',
    'w': '1.0.8'
}
base_url = 'https://sc.chinaz.com/tupian/index_'

if __name__ == "__main__":
    for i in range(2, 2501):
        url = base_url + str(i) + '.html'
        r = requests.get(url, headers=headers)
        r.encoding = 'UTF-8'
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        target_div = soup.find('div', attrs={'class': 'text_left text_lefts'})
        content = target_div.find('div', attrs={'class': 'clearfix psdk imgload'})
        all_items = target_div.find_all('div', attrs={'class': 'box picblock col3'})
        for item in all_items:
            img_url = 'http:' + item.a.img['src2']
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = '../image/chinaz_image/' + str(file_name_index) + '.jpeg'
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)
                file_name_index += 1
            except BaseException:
                cut_logger.info("pull error! skip current image : %s", traceback.format_exc())
            cut_logger.info('当前爬取页面下标：%s,爬取总图片数：%s', i, file_name_index)
    cut_logger.info('pull done!')
