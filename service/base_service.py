# -*- coding:utf-8 -*-
import sys
from util.mysql_util import MysqlUtil,DataBaseUtil
from job.link_job import LinkJob
import threading
import logging as log
import traceback

upt_task_selected = "update %s set selected =%%s where %s = %%s"
upt_task_status = "update %s set status=%%s,nice=%%s,selected =%%s,http_code=%%s where %s =%%s"


class BaseService(object):
    def __init__(self, name, get_task_sql, table_name, primary_key, wrapper_entity, setting):
        self.name = name
        self.batch_size = setting['batch_add_links_size']
        self.setting = setting
        self.get_task_sql = get_task_sql
        self.upt_task_selected = upt_task_selected % (table_name,primary_key)
        self.upt_task = upt_task_status % (table_name,primary_key)
        self.wrapper_entity = wrapper_entity
        self.synchronize_lock = threading.Lock()


    def add_job(self, crawler, category):
        with self.synchronize_lock:
            mysql_util = MysqlUtil()
            link_jobs = mysql_util.select(self.get_task_sql % self.batch_size)
            for item_job in link_jobs:
                try:
                    mysql_util.execute(self.upt_task_selected % (1, item_job[0]))
                    task = self.wrapper_entity(item_job)
                    link_job = LinkJob(task)
                    link_job.set_category(category)
                    crawler.links_queue.put_link(link_job)
                except:
                    # 入队失败回收
                    t, v, tb = sys.exc_info()
                    log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))                    
                    mysql_util.execute(self.upt_task_selected % (0, item_job[0]))
            mysql_util.close()
            log.info("service:%s has completed the add_job,add size:%s!" % (category,len(link_jobs)))

    def update_task(self, status, nice, selected, fetched_date, http_code, task_id):
        if not self.setting['date_need_add']:
            DataBaseUtil.execute(self.upt_task % (status, nice, selected, http_code, task_id))
        else:
            DataBaseUtil.execute(self.upt_task % (status, nice, selected, fetched_date, http_code, task_id))

    def if_has_data(self, content):
        pass

    def parse_content(self, content, link_job):
        pass
