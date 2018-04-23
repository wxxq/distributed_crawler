# -*- coding: utf-8 -*-
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
from service.xq_user_article_service import XQUserArticleService
from service.xq_user_cubes_service import XQUserCubeService
from service.xq_user_stocks_service import XQUserStockService


class Crawler():
    """
    Main Thread
    """

    def __init__(self, setting, services):
        self.proxy_queue = HttpProxyQueue(setting['proxy_frequency_time'])
        self.links_queue = PressureControlQueue(setting["frequency_time"])
        self.pages_queue = Queue()

        self.download_workers = []
        self.extractor_workers = []
        self.proxy_check_workers = []

        self.setting = setting

        self.service = self._init_service(services)

    def start(self):
        self._start_workers()
        self._start_extractors()
        self._start_queue_monitor()
        self._start_proxy_check_workers()

    def _init_service(self, services):
        service_container = {}
        for service in services:
            name = getattr(service, "name")
            service_container[name] = service
        return service_container

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
        # worker.setDaemon(True)
        worker.start()

    # 启动检测http代理的线程
    def _start_new_proxy_checker(self):
        worker = ProxyCheckWorker(self)
        # worker.setDaemon(True)
        worker.start()
        self.proxy_check_workers.append(worker)

    # 启动下载线程
    def _start_new_worker(self):
        worker = DownloadWorker(self)
        # worker.setDaemon(True)
        worker.start()
        self.download_workers.append(worker)

    # 启动解析线程
    def _start_new_extractor(self):
        worker = ExtractorWorker(self)
        # worker.setDaemon(True)
        worker.start()
        self.extractor_workers.append(worker)


if __name__ == "__main__":
    fileConfig("logger_config.ini")
    xq_config = load_config("xq_user_article")
    services = []
    xq_article_service = XQUserArticleService(xq_config)
    xq_cube_service = XQUserCubeService(xq_config)
    xq_stock_service = XQUserStockService(xq_config)
    services.append(xq_article_service)
    services.append(xq_cube_service)
    services.append(xq_stock_service)
    crawler = Crawler(xq_config, services)
    crawler.start()



