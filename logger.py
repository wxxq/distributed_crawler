# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from settings import CATEGORY_LOG




class LoggerHolder(object):


    def __init__(self, setting):
        self.log_name = setting["log_name"]
        self.log_back_count = setting["log_back_count"]
        self.log_level = setting["log_level"]
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        self.suffix = datetime.now().strftime('%Y-%m-%d')
        self.root_logger=self.create_conf(self.log_back_count,self.log_level)

    def create_conf(self, backupCount, level):
        # price logs configure
        root_logger = logging.getLogger()
        if len(root_logger.handlers) == 0:
            root_logger.setLevel(logging.getLevelName(self.log_level))  # Log等级总开关
            category_path = '../logs/%s-%s.txt' % (CATEGORY_LOG, self.suffix)
            category_handler = RotatingFileHandler(category_path, maxBytes=1024 * 1024 * 1024, backupCount=backupCount,mode='w')
            category_handler.setLevel(level)
            category_handler.setFormatter(self.formatter)
            root_logger.addHandler(category_handler)
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(self.formatter)
            root_logger.addHandler(ch)
        return root_logger

    def info(self, msg, *args, **kwargs):
        self.root_logger.info(msg, *args, **kwargs)
# 日志等级   debug 、info 、warning 、error 、critical
