# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import threading
import mycurl
from job.proxy_job import ProxyJob
import logging as log
import json
class ProxyCheckWorker(threading.Thread):
    """
        检测失败的代理是否可以重新使用
    """
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.http_proxy_queue = crawler.proxy_queue
        self.proxy_check_func = getattr(crawler.parse_service,"check_proxy_available")

    def run(self):
        while True:
            proxy_job = self.http_proxy_queue.pop_checked_proxy()
            ip, port = proxy_job.ip, proxy_job.port
            flag = self.proxy_check_func(ip, port)
            if flag:
                self.http_proxy_queue.put_proxy(ProxyJob(ip,port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s ok..." % (threading.current_thread().getName(), ip, port))
            else:
                self.http_proxy_queue.put_checked_proxy(ProxyJob(ip,port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s error..." % (threading.current_thread().getName(), ip, port))
