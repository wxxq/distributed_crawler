# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
from base_task import BaseTask
from copy import copy

url_pattern = "https://xueqiu.com/friendships/followers.json?uid=%s&pageNo=%s"
DOWNLOAD_HEADERS = [
     "Accept:application/json, text/javascript, */*; q=0.01",
     "Accept-Encoding:gzip, deflate, sdch, br",
     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
     "Connection:keep-alive",
     "Host:xueqiu.com",
     "Referer:https://xueqiu.com/people",
    "Cookie:__utmz=1.1521950844.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); device_id=8147d889099b145fc775c0afa66ccf78; s=fz11cvq46z; aliyungf_tc=AQAAAOMxjC41uAYAQoXv26zn8nDN45rg; xq_a_token=229a3a53d49b5d0078125899e528279b0e54b5fe; xq_a_token.sig=oI-FfEMvVYbAuj7Ho7Z9mPjGjjI; xq_r_token=8a43eb9046efe1c0a8437476082dc9aac6db2626; xq_r_token.sig=Efl_JMfn071_BmxcpNvmjMmUP40; u=711522754903243; Hm_lvt_1db88642e346389874251b5a1eded6e3=1521950844,1522683252,1522685277,1522754903; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1522754903; __utma=1.1284817915.1521950844.1522683251.1522754903.3; __utmc=1; __utmt=",
     "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]
class User(BaseTask):

    def __init__(self,sql_entity):
        task_id = sql_entity[0]
        uid = sql_entity[1]
        no = sql_entity[2]
        status = sql_entity[3]
        nice = sql_entity[4]
        selected = sql_entity[5]
        http_code = sql_entity[6]
        level = sql_entity[7]
        self.uid = uid
        self.no = no
        self.level = level
        self.header = self.__create_header()
        BaseTask.__init__(self,task_id,status,nice,selected,http_code,None)
        self.url = self.__create_url()

    def __create_url(self):
        url = url_pattern % (self.uid,self.no)
        return url

    def __create_header(self):
        header = copy(DOWNLOAD_HEADERS)
        # refer="Referer:https://xueqiu.com/u/%s" % self.uid
        # header.append(refer)
        return header


if __name__ == '__main__':
    pass