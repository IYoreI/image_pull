#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/14 15:46
# @Author  : Yore
# @Site    :
# @File    : baidu_image_pull.py
# @Software: PyCharm
import requests
import os, time
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_sogou_image_pull.log'
cut_logger = get_logger(path, 'sogou_image_pull')

url = 'https://pic.sogou.com/napi/pc/searchList?'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
request_param = {
    'mode': '1',
    'xml_len': '48'
}

if __name__ == '__main__':
    each_category_num = 2000
    # categoreis = ['壁纸','生活','汽车','风景','建筑','人物','交通工具','旅游','美女','球','动物']
    categoreis = ['生活', '汽车', '风景', '建筑', '人物', '交通工具', '旅游', '美女', '球', '动物']
    for category in categoreis:
        index = 1
        dir = '../image/sogou_image/' + category
        if (not os.path.exists(dir)):
            os.makedirs(dir)
        while index < each_category_num:
            request_param['start'] = index
            request_param['query'] = category

            page_text = requests.get(url=url, headers=header, params=request_param)
            page_text.encoding = 'utf-8'
            page_text = page_text.json()

            info_list = page_text['data']['items']

            img_path_list = []
            for i in info_list:
                img_path_list.append(i['oriPicUrl'])
            for img_path in img_path_list:
                try:
                    img_data = requests.get(url=img_path, headers=header).content
                    img_path = dir + '/' + str(index) + '.jpeg'
                    with open(img_path, 'wb') as fp:
                        fp.write(img_data)
                    index += 1
                except BaseException:
                    print("pull error! skip current image")
            cut_logger.info('category: %s pull count= %s', category, index)
            time.sleep(1)
        cut_logger.info(' category: %s pull done,  count= %s', category, index)

