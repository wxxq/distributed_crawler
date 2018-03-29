database = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'xueqiu'
}


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
