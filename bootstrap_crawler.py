#-*- coding: utf-8 -*-
from Queue import Queue

from core.download_worker import DownloadWorker
from core.extractor_worker import ExtractorWorker
from core.proxy_check_worker import ProxyCheckWorker
from core.queue_monitor import QueueMonitor
from queue.pressure_queue import PressureControlQueue
from queue.http_proxy_queue import HttpProxyQueue
from load_config import load_config
from logging.config import fileConfig
from service.xq_user_article_service import XQUserArticleService
from service.xq_user_article_parse_service import XQUserArticleParseService

class Crawler():
    """
    Main Thread
    """
    def __init__(self,setting,service,parse_service):
        self.proxy_queue    = HttpProxyQueue(setting['proxy_frequency_time'])
        self.links_queue    = PressureControlQueue(setting["frequency_time"])
        self.pages_queue    = Queue()

        self.threads    = []
        self.runable    = True
        self.download_workers   = []
        self.extractor_workers  = []

        self.setting = setting
        self.service = service
        self.parse_service = parse_service

    def start(self):
        self._start_workers()
        self._start_extractors()
        self._start_queue_monitor()
        self._start_proxy_check_workers()



    def _start_workers(self):
        for _ in range(self.setting['download_workers_size']):
            self._start_new_worker()

    def _start_extractors(self):
        for _ in range(self.setting['extractor_workers_size']):
            self._start_new_extractor()

    def _start_queue_monitor(self):
        self._start_monitor()

    def _start_proxy_check_workers(self):
        for _ in range(self.setting['proxy_checker_size']):
            self._start_new_proxy_checker()

    def _start_monitor(self):
        worker = QueueMonitor(self)
        #worker.setDaemon(True)
        worker.start()
        self.threads.append(worker)


    #启动检测http代理的线程
    def _start_new_proxy_checker(self):
        worker = ProxyCheckWorker(self)
        #worker.setDaemon(True)
        worker.start()
        self.threads.append(worker)

    #启动下载线程
    def _start_new_worker(self):
        worker = DownloadWorker(self)
        #worker.setDaemon(True)
        worker.start()
        self.download_workers.append(worker)

    #启动解析线程
    def _start_new_extractor(self):
        worker = ExtractorWorker(self)
        #worker.setDaemon(True)
        worker.start()
        self.extractor_workers.append(worker)


if __name__ == "__main__":
    fileConfig("logger_config.ini")
    xq_config=load_config("xq_user_article")
    xq_service = XQUserArticleService(xq_config)
    xq_parse_service = XQUserArticleParseService(xq_config)
    crawler = Crawler(xq_config,xq_service,xq_parse_service)
    crawler.start()
