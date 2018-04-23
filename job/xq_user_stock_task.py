# -*- coding:utf-8 -*-
import sys

sys.path.append('..')
from base_task import BaseTask
from copy import copy

DOWNLOAD_HEADERS = [
     "Upgrade-Insecure-Requests:1",
     "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
     "Accept-Encoding:gzip, deflate, sdch, br",
     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
     "Cache-Control:max-age=0",
     "Connection:keep-alive",
     "Host:xueqiu.com",
     "Cookie:__utma=1.1299756509.1521955892.1524031139.1524127246.32; __utmz=1.1522137777.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; aliyungf_tc=AQAAAOhjwRDk7wEAqbEbd+AUjwN6S5dQ; xq_a_token=0d524219cf0dd2d0a4d48f15e36f37ef9ebcbee1; xq_a_token.sig=P0rdE1K6FJmvC2XfH5vucrIHsnw; xq_r_token=7095ce0c820e0a53c304a6ead234a6c6eca38488; xq_r_token.sig=xBQzKLc4EP4eZvezKxqxXNtB7K0; u=231524468913763; Hm_lvt_1db88642e346389874251b5a1eded6e3=1524127245,1524468511,1524468798,1524468914; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1524468914; device_id=e24f3c89cceb3d13f617ecfcc0611357",
     "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]

class UserStock(BaseTask):
    url_pattern = "https://xueqiu.com/v4/stock/portfolio/stocks.json?size=10000&type=1&pid=-1&category=2&uid=%s"

    def __init__(self, sql_entity):
        task_id = sql_entity[0]
        uid = sql_entity[1]
        status = sql_entity[2]
        nice = sql_entity[3]
        selected = sql_entity[4]
        http_code = sql_entity[5]
        self.uid = uid
        self.header = self.__create_header()
        BaseTask.__init__(self, task_id, status, nice, selected, http_code, None)
        self.url = self.__create_url()

    def __create_url(self):
        url = self.url_pattern % ( self.uid)
        return url

    def __create_header(self):
        header = copy(DOWNLOAD_HEADERS)
        # refer="Referer:https://xueqiu.com/u/%s" % self.uid
        # header.append(refer)
        return header
