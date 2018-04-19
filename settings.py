database = {
    'host': '172.16.24.203',
    'user': 'data',
    'passwd': 'opensesame',
    'db': 'xueqiu'
}

mongo_database = {
    'host':'172.16.24.207',
    'port':27017,
    'db':'xueqiu'
}
#
# redis_db = {
#     'host':'172.16.24.209',
#     'port':6379
# }
# database = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'passwd': '',
#     'db': 'xueqiu'
# }
#
# mongo_database = {
#     'host':'192.168.133.130',
#     'port':27017,
#     'db':'xueqiu'
# }

redis_db = {
    'host':'192.168.133.130',
    'port':6379
}

OK_CODE         = 200
REDIRECT_CODE   = 302
NO_CONTENT      = 204
NOT_FOUND       = 404

STATUS_OK           = 1
STATUS_ERROR        = 2
STATUS_NOT_FOUND    = 3

DOWNLOAD_HEADERS = [
     "Accept:*/*",
     "Accept-Encoding:gzip, deflate, sdch", 
     "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
     "Connection:keep-alive",
     "Referer:https://kyfw.12306.cn/otn/leftTicket/init",
     "X-Requested-With:XMLHttpRequest",
     "Host: kyfw.12306.cn"
]

PC_USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]

PC_USER_AGENTS_SUM = len(PC_USER_AGENTS)
