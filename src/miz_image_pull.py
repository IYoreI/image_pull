#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/17 16:33
# @Author  : Yore
# @Site    : 
# @File    : miz_image_pull.py
# @Software: PyCharm

import requests
import os, time
from bs4 import BeautifulSoup

import traceback
from src.logger import get_logger

my_time = time.strftime("%Y-%m-%d", time.localtime())
path = '../logs/' + my_time + '_51miz_image_pull.log'
cut_logger = get_logger(path, '51miz_image_pull')

file_name_index = 161331

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'couponSign=1; QuDao=61; ustk=202109171632_1908977164_881229582; seoChannel=1; ufrom=41; semplan=1; semunit=1; semkeywordid=1; semsource=1; is_beijing=-1; Qs_lvt_158497=1631867538; Hm_lvt_d8453059bf561226f5e970ffb07bd9d2=1631867538; Hm_lvt_aa0de2c55d65303b7191698178841e01=1631867538; Hm_lvt_819233eaec5f3d414484d07a53aba86a=1631867538; Hm_lpvt_d8453059bf561226f5e970ffb07bd9d2=1631867726; Hm_lpvt_aa0de2c55d65303b7191698178841e01=1631867726; Qs_pv_158497=1999791792764919800%2C2864747168680165400%2C2006770161134930400%2C3731460695899660300%2C4498015736146931000; Hm_lpvt_819233eaec5f3d414484d07a53aba86a=1631867726; backurl=https%3A%2F%2Fwww.51miz.com%2Fso-tupian%2F217793%2Fp_3%2F',
    'Connection': 'keep-alive',
    # 'keyword': '长图',
    # 'keyword_id': '217793',
    'plate_id': '3',
    'm': 'userSuggest',
    'plate_path':'tupian',
    'issearch':'1',
    'ajax': '1'
}
base_url = 'https://www.51miz.com/tupian/p_'
# base_url = 'https://www.51miz.com/so-tupian/85064/p_'

if __name__ == "__main__":
    for i in range(1, 2000):
        url = base_url + str(i) + '/'
        headers['page'] = str(i)
        r = requests.get(url, headers=headers)
        r.encoding = 'UTF-8'
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        target_div = soup.find('div', attrs={'class': 'main-content oh pr'})
        content = target_div.find('div', attrs={'class': 'flex-images pr'})
        all_items = target_div.find_all('div', attrs={'class': 'element-box item real-box'})
        for item in all_items:
            item = item.find('div', attrs={'class': 'element-box-detail'}).find('div', attrs={'class': 'element pr oh'})
            img_url = 'http:' + item.a.img['data-original']
            img_url = img_url[0:img_url.find('!')]
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_path = '../image/51miz_image/' + str(file_name_index) + '.jpeg'
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)
                file_name_index += 1
            except BaseException:
                cut_logger.info("pull error! skip current image : %s", traceback.format_exc())
            cut_logger.info('当前爬取页面下标：%s,爬取总图片数：%s', i, file_name_index)
    cut_logger.info('pull done! current file index:%s', file_name_index)
