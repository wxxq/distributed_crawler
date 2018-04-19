# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import threading
import time
from job.proxy_job import ProxyJob
from util.data_service import DataService
import logging as log
class QueueMonitor(threading.Thread):

    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.crawler = crawler
        self.add_job_func = getattr(crawler.service,"add_job")
        self.min_link_size = crawler.setting['links_queue_min_size']
        self.download_work_size = crawler.setting['download_workers_size']
        self.runable = True

    def run(self):
        while True:
            try:
                #1、统计队列中任务数量
                self.__collect_qsizes()
                #2、检测抓取与抽取线程数量
                self.__check_worker_size()
                #3、增加新抓取任务
                self.__check_links_queue()
                if self.crawler.setting['if_use_proxy']:
                    #4、发现新代理，提供给代理队列
                    self.__check_proxy_queue()
                    #5、统计队列中代理数量
                    self.__collect_proxy_sizes()
            except:
                import sys, traceback
                t, v, tb = sys.exc_info()
                #print "Queue Monitor Error: %s,%s,%s" % (t, v, traceback.format_tb(tb))
                print t, v, tb
            finally:
                time.sleep(10)
    
    
    def __check_links_queue(self):
        self.add_job_func(self.crawler,self.min_link_size)

                    
    def __collect_qsizes(self):
        log.info("links_queue: %s" % self.crawler.links_queue.statics())

    def __collect_proxy_sizes(self):
        log.info("proxy_queue: %s" % self.crawler.proxy_queue.statics())
        
    def __check_worker_size(self):
        worker_count = 0
        for i in range(len(self.crawler.download_workers)):
            if not self.crawler.download_workers[i].is_alive():
                del  self.crawler.download_workers[i]
                i -=1
            else:
                worker_count += 1
        if worker_count < self.download_work_size:
            log.info("Create a new worker, because there are only %d workers left" % worker_count)
            self.crawler._start_new_worker()

    '''加入新的http代理IP'''
    def __check_proxy_queue(self):
        proxy_jobs =DataService.select_proxy()
        DataService.update_proxys()
        for proxy in proxy_jobs :
            proxy_job = ProxyJob(proxy[1], proxy[2])
            self.crawler.proxy_queue.put_checked_proxy(proxy_job)

        
        
        
        
        