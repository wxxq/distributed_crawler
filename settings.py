# -*- coding: utf-8 -*-
import time,datetime
# date to str
fetch_date= (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

# 日志的类型
# CATEGORY_LOG = 'dp-shop'
CATEGORY_LOG = 'station-12306'
#抓取间隔
FREQUENCY_TIME = 5

#是否需要增加日期
DATE_NEED_ADD = False

#是否使用代理
IF_USE_PROXY = False 

#代理使用
PROXY_FREQUENCY_TIME = 10

#通信状态
OK_CODE         = 200
REDIRECT_CODE   = 302
NO_CONTENT      = 204
NOT_FOUND       = 404

STATUS_OK           = 1
STATUS_ERROR        = 2
STATUS_NOT_FOUND    = 3

# nice 最大值设置
CATCH_NUM = 20

DOWNLOAD_WORKERS_SIZE = 1
EXTRACTOR_WORKERS_SIZE =4
PROXY_CHECKER_SIZE = 0 
LINKS_QUEUE_MIN_SIZE = 512

BATCH_ADD_LINKS_SIZE = 256

#代理检测链接
check_url = "http://www.ly.com/huochepiao/Handlers/TrainListSearch.ashx?to=baigou&from=tielingxi&trainDate=2017-04-22&PlatId=1&callback=jQuery183004485401697308511"

# check_url = "http://mapi.dianping.com/searchshop.json?start=0&regionid=0&categoryid=10&cityid=2&locatecityid=2&maptype=0"
# check_url = "http://catfront.dianping.com/api/batch?v=1&sdk=1.4.31"

# check_heades  = [
#     "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
#     "Connection: close",
#     "Host: www.dianping.com",
#     "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
#     "Upgrade-Insecure-Requests:1"]
check_heades = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset: utf-8, gbk*,*",
    "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    "Connection: close",
    "Host: www.ly.com",
    "Via: WTP/1.1 HBWH-PS-WAP-GW11.hbwh.monternet.com (Nokia WAP Gateway 4.0/CD3/4.1.79)",
    "X-Forwarded-For: 127.0.0.1",
]

# database = {
#     'host': '172.16.24.203',
#     'user': 'data',
#     'passwd': 'opensesame',
#     'db': 'xueqiu'
# }

database = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'xueqiu'
}
# database = {
#     'host': '192.100.2.31',
#     'user': 'data',
#     'passwd': 'opensesame',
#     'db': 'traincrawler'
# }

#DOWNLOAD_HEADERS = [
#    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Charset: utf-8, gbk*,*",
#    "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
#    "Connection: close",
#    "Host: www.ly.com",
#    "Via: WTP/1.1 HBWH-PS-WAP-GW11.hbwh.monternet.com (Nokia WAP Gateway 4.0/CD3/4.1.79)",
#    "X-Forwarded-For: 127.0.0.1",
#]

DOWNLOAD_HEADERS = [
     "Accept:*/*",
     "Accept-Encoding:gzip, deflate, sdch", 
     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
     "Connection:keep-alive",
     "Referer:https://kyfw.12306.cn/otn/leftTicket/init",
     "X-Requested-With:XMLHttpRequest",
     "Host: kyfw.12306.cn"
]


# DOWNLOAD_HEADERS = [
#     "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
#     "Connection: close",
#     "Host: www.dianping.com",
#     "Upgrade-Insecure-Requests:1",
#     "Cookie:_hc.v=\"\"8e472d46-41cf-4dbc-9267-63ffa3b49e8d.1495254300\"\"; PHOENIX_ID=0a010444-15c2419f777-f1114c8; JSESSIONID=3C6AC9006AD26231205475F2C61FA8FA; aburl=1; cy=2; cye=beijing; __mta=46464664.1495254306523.1495254306523.1495254306523.1"
# ]


PC_USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]

PC_USER_AGENTS_SUM = len(PC_USER_AGENTS)
