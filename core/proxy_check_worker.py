# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import threading
import mycurl
from job.proxy_job import ProxyJob
import logging as log
import json
import traceback


class ProxyCheckWorker(threading.Thread):
    """
        检测失败的代理是否可以重新使用
    """

    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.setting = crawler.setting
        self.http_proxy_queue = crawler.proxy_queue

    def run(self):
        while True:
            proxy_job = self.http_proxy_queue.pop_checked_proxy()
            ip, port = proxy_job.ip, proxy_job.port
            flag = self.check_proxy_available(ip, port)
            if flag:
                self.http_proxy_queue.put_proxy(ProxyJob(ip, port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s ok..." % (
                    threading.current_thread().getName(), ip, port))
            else:
                self.http_proxy_queue.put_checked_proxy(ProxyJob(ip, port))
                log.info("ProxyCheckWorker thread_name = %s, check proxy usable %s:%s error..." % (
                    threading.current_thread().getName(), ip, port))

    def check_proxy_available(self, ip, port):
        response, flag = None, False
        try:
            response = mycurl.get(self.setting['check_url'], request_headers=self.setting['check_headers'], timeout=10,
                                  proxy="%s:%s" % (ip, port))
            if response and response.status == 200:
                flag = True
        except:
            t, v, tb = sys.exc_info()
            log.debug("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
        return flag
