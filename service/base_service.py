# -*- coding:utf-8 -*-
import sys
from util.mysql_util import DataBaseUtil
from job.link_job import LinkJob

upt_task_selected = "update %s set selected =%%s where task_id = %%s"
upt_task_status = "update %s set status=%%s,nice=%%s,selected =%%s,http_code=%%s where task_id =%%s"


class BaseService(object):
    def __init__(self, get_task_sql,table_name, wrapper_entity, setting):
        self.batch_size = setting['batch_add_links_size']
        self.setting = setting
        self.get_task_sql = get_task_sql
        self.upt_task_selected = upt_task_selected % table_name
        self.upt_task = upt_task_status % table_name
        self.wrapper_entity = wrapper_entity

    def add_job(self, crawler, min_link_size):
        if crawler.links_queue.qsize <= min_link_size:
            link_jobs = DataBaseUtil.select(self.get_task_sql % self.batch_size)
            # 取出数据的同时更新selected状态
            for job in link_jobs:
                DataBaseUtil.execute(self.upt_task_selected % (1, job[0]))
            for item_job in link_jobs:
                try:
                    task = self.wrapper_entity(item_job)
                    link_job = LinkJob(task)
                    crawler.links_queue.put_link(link_job)
                except:
                    # 入队失败回收
                    DataBaseUtil.execute(self.upt_task_selected % (0, item_job[0]))

    def update_task(self, status, nice, selected, fetched_date, http_code, task_id):
        if not self.setting['date_need_add']:
            DataBaseUtil.execute(self.upt_task % (status, nice, selected, http_code, task_id))
        else:
            DataBaseUtil.execute(self.upt_task % (status, nice, selected, fetched_date, http_code, task_id))
