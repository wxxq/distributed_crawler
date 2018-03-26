#-*- coding:utf-8 -*-

import sys
sys.path.append('..')
from base_setting import BaseSetting

CATEGORY_LOG = 'station-12306'

FREQUENCY_TIME = 5

#是否需要增加日期
DATE_NEED_ADD = False

#是否使用代理
IF_USE_PROXY = False

#代理使用
PROXY_FREQUENCY_TIME = 10

# nice 最大值设置
CATCH_NUM = 20

DOWNLOAD_WORKERS_SIZE = 16
EXTRACTOR_WORKERS_SIZE = 10
PROXY_CHECKER_SIZE = 5
LINKS_QUEUE_MIN_SIZE = 12288

BATCH_ADD_LINKS_SIZE = 4096

CHECK_URL = "https://www.ly.com/uniontrain/trainapi/TrainPCCommon/SearchTrainRemainderTickets?callback=jQuery1830414364584783371_1499395892747&para={%22To%22:%22%E5%B9%BF%E5%B7%9E%22,%22From%22:%22%E5%93%88%E5%B0%94%E6%BB%A8%22,%22TrainDate%22:%222017-07-25%22,%22PassType%22:%22%22,%22TrainClass%22:%22%22,%22FromTimeSlot%22:%22%22,%22ToTimeSlot%22:%22%22,%22FromStation%22:%22%22,%22ToStation%22:%22%22,%22SortBy%22:%22fromTime%22,%22callback%22:%22%22,%22tag%22:%22%22,%22memberId%22:%220%22,%22headct%22:%220%22,%22platId%22:1,%22headver%22:%221.0.0%22,%22headtime%22:1499395893673}"

DOWNLOAD_HEADERS = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control:max-age=0",
    "Connection:keep-alive",
    "Host: www.ly.com",
    "Upgrade-Insecure-Requests:1"
]

CHECK_HEADERS = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control:max-age=0",
    "Connection:keep-alive",
    "Host: www.ly.com",
    "Upgrade-Insecure-Requests:1",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
]

class TicketPriceSetting(BaseSetting):

    def __init__(self):
        obj = {}
        obj['category_log']=CATEGORY_LOG
        obj['frequency_time']=FREQUENCY_TIME
        obj['date_need_add']=DATE_NEED_ADD
        obj['if_user_proxy']=IF_USE_PROXY
        obj['proxy_frequency_time']=PROXY_FREQUENCY_TIME
        obj['catch_num']=CATCH_NUM
        obj['download_workers_size']=DOWNLOAD_WORKERS_SIZE
        obj['extractor_workers_size']=EXTRACTOR_WORKERS_SIZE
        obj['proxy_checker_size']=PROXY_CHECKER_SIZE
        obj['links_queue_min_size']=LINKS_QUEUE_MIN_SIZE
        obj['batch_add_links_size']=BATCH_ADD_LINKS_SIZE
        obj['check_url']=CHECK_URL
        obj['download_headers']=DOWNLOAD_HEADERS
        obj['check_headers']=CHECK_HEADERS
        BaseSetting.__init__(self,obj)