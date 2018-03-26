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
     "Cookie:device_id=ba3446e3ab3cc2a3d054390b137193c1; s=ff1wtme8sq; aliyungf_tc=AQAAAGPTC1LoyA4AQoXv23YF70Se08ad; xq_a_token=19f5e0044f535b6b1446bb8ae1da980a48bbe850; xq_a_token.sig=aaTVFAX9sVcWtOiu-5L8dL-p40k; xq_r_token=6d30415b5f855c12fd74c6e2fb7662ea40272056; xq_r_token.sig=rEvIjgpbifr6Q_Cxwx7bjvarJG0; u=471521803224051; __utmt=1; __utma=1.16239544.1521706461.1521771357.1521803224.3; __utmb=1.2.10.1521803224; __utmc=1; __utmz=1.1521803224.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1521706460,1521771357,1521803224; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1521803232",
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
        self.uid = uid
        self.no = no
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