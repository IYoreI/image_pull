#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/14 19:49
# @Author  : Yore
# @Site    :
# @File    : netbian_image_pull.py
# @Software: PyCharm


import requests
import os, time

from pyquery import PyQuery as pq

file_num = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '__yjs_duid=1_c2e0268535865c21e9b5709e8856a9981631751511828; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1631751504; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1631751560',
    'Upgrade-Insecure-Requests': '1'
}

def parse(text, path, i):
    global file_num

    # bf = BeautifulSoup(text, 'lxml')
    # img_url = bf.find('div', class_='list').find('img').get('src')

    doc = pq(text)
    # 锁定页面中的img标签
    images = doc('div.list ul li img').items()
    count = 1
    for image in images:
        img_url = image.attr('src')
        img = requests.get(img_url, headers=headers).content
        file = path + str(file_num) + '.jpeg'
        with open(file, 'wb') as f:
            f.write(img)
            time.sleep(1)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' current epoch:', i, 'download image:', count)
            count += 1
        file_num += 1


if __name__ == "__main__":

    path = '../image/netbian_image/'
    for i in range(51, 1200):
        url = 'http://www.netbian.com/index_' + str(i) + '.htm'
        r = requests.get(url, headers=headers)
        r.encoding = 'GBK'
        text = r.text
        parse(text, path, i)
        time.sleep(5)
