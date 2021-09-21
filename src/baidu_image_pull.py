#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/14 15:46
# @Author  : Yore
# @Site    : 
# @File    : baidu_image_pull.py
# @Software: PyCharm
import requests
import os
import time

from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_baidu_image_pull.log'
cut_logger = get_logger(path, 'baidu_image_pull')

url = 'https://image.baidu.com/search/acjson?'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
request_param = {
    'tn': 'resultjson_com',
    'logid': '8846269338939606587',
    'ipn': 'rj',
    'ct': '201326592',
    'is': '',
    'fp': 'result',
    # 'queryWord': '',
    'cl': '2',
    'lm': '-1',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'adpicid': '',
    'st': '-1',
    'z': '',
    'ic': '',
    'hd': '',
    'latest': '',
    'copyright': '',
    # 'word': '',
    's': '',
    'se': '',
    'tab': '',
    'width': '',
    'height': '',
    'face': '0',
    'istype': '2',
    'qc': '',
    'nc': '1',
    'fr': '',
    'expermode': '',
    'force': '',
    'cg': '',
    # 'pn': pn,
    'rn': '30',
    'gsm': '1e',
}

if __name__ == '__main__':
    each_category_num = 50000
    # categoreis = ['生活','汽车','风景','建筑','人物','交通工具','旅游','美女','球','动物']

    categoreis = ['壁纸']
    for category in categoreis:
        pn = 1
        request_param['pn'] = pn
        request_param['queryWord'] = category
        request_param['word'] = category
        page_text = requests.get(url=url, headers=header, params=request_param)
        page_text.encoding = 'utf-8'
        page_text = page_text.json()
        info_list = page_text['data']
        del info_list[-1]
        img_path_list = []
        index = 1
        dir = '../image/baidu_image/' + category
        if (not os.path.exists(dir)):
            os.makedirs(dir)

        while index < each_category_num:
            for i in info_list:
                img_path_list.append(i['thumbURL'])
            for img_path in img_path_list:
                try:
                    img_data = requests.get(url=img_path, headers=header).content
                    img_path = dir + '/' + str(index) + '.jpeg'
                    with open(img_path, 'wb') as fp:
                        fp.write(img_data)
                    index += 1
                except BaseException:
                    print("pull error! skip current image")

            pn += 29
            cut_logger.info('category: %s pull count= %s', category, index)
            time.sleep(3)
        cut_logger.info(' category: %s pull done,  count= %s', category, index)
