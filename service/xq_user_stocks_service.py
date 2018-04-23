# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.xq_user_stock_task import UserStock
from util.mongo_util import MongoUtil
from util.mysql_util import DataBaseUtil
import json


class XQUserStockService(BaseService):
    get_task_sql = "select id,user_id,status, nice, selected, http_code from task_user_stocks WHERE selected = 0 and nice = 0 LIMIT %s"

    def __init__(self, setting):
        self.name = "task_user_stocks"
        self.primary_key ="id"
        BaseService.__init__(self, self.name, self.get_task_sql, self.name, self.primary_key, UserStock, setting)

    def if_has_data(self, content):
        if content:
            try:
                i = content.index('stocks')
                return True
            except:
                pass
        return False

    def parse_content(self, content, link_job):
        task = link_job.task
        user_id = task.uid
        data = json.loads(content)
        stocks = data['stocks']
        for item in stocks:
            item["user_id"] = user_id
            MongoUtil.insert('xq_user_stock', item)
