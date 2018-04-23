# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
import threading
import time
from job.proxy_job import ProxyJob
from util.mysql_util import MysqlUtil
import logging as log


class QueueMonitor(threading.Thread):
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.crawler = crawler
        self.download_work_size = crawler.setting['download_workers_size']
        self.line_task_size = crawler.setting["links_queue_min_size"]
        self.runable = True

    def run(self):
        while True:
            try:
                # 1、统计队列中任务数量
                self.__collect_qsizes()
                # 2、检测抓取与抽取线程数量
                self.__check_worker_size()
                # 3、增加新抓取任务
                self.__produce_links()
                if self.crawler.setting['if_use_proxy']:
                    # 4、发现新代理，提供给代理队列
                    self.__check_proxy_queue()
                    # 5、统计队列中代理数量
                    self.__collect_proxy_sizes()
            except:
                import sys, traceback
                t, v, tb = sys.exc_info()
                # print "Queue Monitor Error: %s,%s,%s" % (t, v, traceback.format_tb(tb))
                print t, v, tb
            finally:
                time.sleep(10)

    def __produce_links(self):
        if self.crawler.links_queue.qsize <= self.line_task_size:
            tmp_thread_contain = []
            for key in self.crawler.service:
                service_instance = self.crawler.service[key]
                add_job_func = getattr(service_instance, "add_job")
                t1 = threading.Thread(target=add_job_func, args=(self.crawler, key), name=key)
                t1.start()
                tmp_thread_contain.append(t1)
            for item_thread in tmp_thread_contain:
                item_thread.join()
            log.info("the whole adding task job have completed,current size:%s!" % self.crawler.links_queue.statics())

    def __collect_qsizes(self):
        log.info("links_queue: %s" % self.crawler.links_queue.statics())

    def __collect_proxy_sizes(self):
        log.info("proxy_queue: %s" % self.crawler.proxy_queue.statics())

    def __check_worker_size(self):
        log.debug("current running download-worker size:%s" % len(self.crawler.download_workers))
        for i in range(len(self.crawler.download_workers)):
            if not self.crawler.download_workers[i].is_alive():
                del self.crawler.download_workers[i]
                log.info("Create a new download_worker.")
                self.crawler._start_new_worker()
        log.debug("current running extractor-worker size:%s" % len(self.crawler.extractor_workers))
        for i in range(len(self.crawler.extractor_workers)):
            if not self.crawler.extractor_workers[i].is_alive():
                del self.crawler.extractor_workers[i]
                log.info("Create a new extractor_worker.")
                self.crawler._start_new_extractor()
        log.debug("current running proxy-check-worker size:%s" % len(self.crawler.proxy_check_workers))
        for i in range(len(self.crawler.proxy_check_workers)):
            if not self.crawler.proxy_check_workers[i].is_alive():
                del self.crawler.proxy_check_workers[i]
                log.info("Create a new proxy_check_worker.")
                self.crawler._start_new_proxy_checker()

    def __check_proxy_queue(self):
        mysql_util = MysqlUtil()
        sql_proxy = 'select id,ip,port from train_proxy where is_use=0 group by ip'
        update_proxy_state = 'update train_proxy set is_use =1 where id = %s'
        proxies = mysql_util.select(sql_proxy)
        for proxy in proxies:
            mysql_util.execute(update_proxy_state%proxy[0])
            proxy_job = ProxyJob(proxy[1], proxy[2])
            self.crawler.proxy_queue.put_checked_proxy(proxy_job)
        mysql_util.close()
