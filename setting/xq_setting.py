#-*- coding:utf-8 -*-

from base_setting import BaseSetting

CATEGORY_LOG = 'xueqiu_user'

STORE_PATH = 'E:/xueqiu/%s-%s.json'

FREQUENCY_TIME = 0.1

#是否需要增加日期
DATE_NEED_ADD = False

#是否使用代理
IF_USE_PROXY = False

#代理使用
PROXY_FREQUENCY_TIME = 10

# nice 最大值设置
CATCH_NUM = 10

DOWNLOAD_WORKERS_SIZE = 10
EXTRACTOR_WORKERS_SIZE = 1

PROXY_CHECKER_SIZE = 16
LINKS_QUEUE_MIN_SIZE = 10240

BATCH_ADD_LINKS_SIZE = 1024

CHECK_URL = "https://xueqiu.com/"



CHECK_HEADERS = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch, br",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control:max-age=0",
    "Connection:keep-alive",
    "Cookie:device_id=ba3446e3ab3cc2a3d054390b137193c1; s=ff1wtme8sq; xq_a_token=19f5e0044f535b6b1446bb8ae1da980a48bbe850; xq_a_token.sig=aaTVFAX9sVcWtOiu-5L8dL-p40k; xq_r_token=6d30415b5f855c12fd74c6e2fb7662ea40272056; xq_r_token.sig=rEvIjgpbifr6Q_Cxwx7bjvarJG0; u=211521855249865; aliyungf_tc=AQAAAHcxsG0HMAIAQoXv24hRR+GDm20a; __utmt=1; __utma=1.16239544.1521706461.1521875455.1521883340.10; __utmb=1.2.10.1521883340; __utmc=1; __utmz=1.1521855250.8.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1521771357,1521803224,1521816380,1521855250; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1521883353",
    "Host:xueqiu.com",
    "Referer:https://xueqiu.com/u/4731243626",
    "Upgrade-Insecure-Requests:1",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]

class XQSetting(BaseSetting):

    def __init__(self):
        obj = {}
        obj['category_log']=CATEGORY_LOG
        obj['frequency_time']=FREQUENCY_TIME
        obj['date_need_add']=DATE_NEED_ADD
        obj['if_use_proxy']=IF_USE_PROXY
        obj['proxy_frequency_time']=PROXY_FREQUENCY_TIME
        obj['catch_num']=CATCH_NUM
        obj['download_workers_size']=DOWNLOAD_WORKERS_SIZE
        obj['extractor_workers_size']=EXTRACTOR_WORKERS_SIZE
        obj['proxy_checker_size']=PROXY_CHECKER_SIZE
        obj['links_queue_min_size']=LINKS_QUEUE_MIN_SIZE
        obj['batch_add_links_size']=BATCH_ADD_LINKS_SIZE
        obj['check_url']=CHECK_URL
        obj['check_headers']=CHECK_HEADERS
        obj['store_path'] = STORE_PATH
        self.obj = obj
        BaseSetting.__init__(self,obj)

    def __getitem__(self,key):
        return self.obj[key]