# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.xq_user_task import User
from util.mongo_util import MongoUtil
from util.redis_util import RedisUtil
from job.link_job import Userjob
import threading
import os
import logging as log
from bson.objectid import ObjectId
import traceback

# 雪球
get_task_sql = "select task_id,user_id,page_no,status, nice, selected, http_code,level from task_user WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_xq_task_selected = "update task_user set selected =%s where task_id = %s"
upt_xq_task = "update task_user set status=%s,nice=%s,selected =%s,http_code=%s where task_id =%s"


class XQService(BaseService):
    def __init__(self, setting):
        BaseService.__init__(self, get_task_sql, upt_xq_task_selected, upt_xq_task, User, setting)
        self.user_batch_size = setting['user_batch_add_links_size']
        self.min_user_size = self.setting['min_user_queue_size']
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../persistence/mongo_id'))
        self.parsed_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../persistence/parsed_mongo_id'))
        self.dead_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../persistence/dead_mongo_ids'))
        self.is_first_start = True

    def add_user(self, crawler):
        if crawler.user_check_queue.qsize < self.min_user_size:
            mongo_id, is_first_init = self._get_placeholder(crawler)
            cursor, last_id = None, None
            if is_first_init:
                cursor = MongoUtil.find("xq_user", {"_id": {"$gte": ObjectId(mongo_id)}},
                                        {"_id": 1, "id": 1, "level": 1, "followers_count": 1}, self.user_batch_size)
            else:
                cursor = MongoUtil.find("xq_user", {"_id": {"$gt": ObjectId(mongo_id)}},
                                        {"_id": 1, "id": 1, "level": 1, "followers_count": 1}, self.user_batch_size)
            for item in cursor:
                last_id = str(item["_id"])
                followers_count = item["followers_count"]
                if followers_count > 0:
                    exists = RedisUtil.get(last_id)
                    if not exists:
                        log.info("user_id:%s have add into the user queue!" % item["id"])
                        crawler.user_check_queue.put_link(Userjob(item))
            self._rw_mongo_id(self.path, 'w', last_id)

    def _get_placeholder(self, crawler):
        is_first_init = None
        mongo_id = None
        with self.lock:
            if self.is_first_start:
                if not os.path.exists(self.path):
                    mongo_id = MongoUtil.find_first_id("xq_user", {}, {"_id": 1, "id": 1})
                    self._rw_mongo_id(self.path, "w", mongo_id)
                    self._rw_mongo_id(self.parsed_path, "w", mongo_id)
                    is_first_init = 1
                else:
                    parsed_mongo_id = self._rw_mongo_id(self.parsed_path, "r")
                    if parsed_mongo_id:
                        mongo_id = parsed_mongo_id
                    else:
                        mongo_id = self._rw_mongo_id(self.path, "r")
                    # self._resurgence_dead_mongo_ids(crawler)
                    is_first_init = 0
                self.is_first_start = False
            else:
                mongo_id = self._rw_mongo_id(self.path, "r")
                is_first_init = 0
        return mongo_id, is_first_init

    def _rw_mongo_id(self, path, model, content=None):
        try:
            f = open(path, model)
            return_content = None
            with f:
                if model == "r":
                    return_content = f.read()
                    return return_content
                elif model == "w":
                    f.write(content)
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
            return None

    def _resurgence_dead_mongo_ids(self,crawler):
        with self.lock2:
            if os.path.exists(self.dead_path):
                content = self._rw_mongo_id(self.dead_path, "r")
                if content:
                    user_jobs = content.split("\n")
                    for item in user_jobs:
                        arr = item.strip().split(",")
                        user_job = {}
                        user_job["_id"] = arr[0]
                        user_job["id"] = arr[1]
                        user_job["level"] = arr[2]
                        u = Userjob(user_job)
                        crawler.user_check_queue.put_link(u)
                self._rw_mongo_id(self.dead_path, "w","")
