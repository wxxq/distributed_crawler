# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.xq_user_article_task import UserArticle
from util.mongo_util import MongoUtil
from util.mysql_util import DataBaseUtil, MysqlUtil
import json


class XQUserArticleService(BaseService):
    get_task_sql = "select task_id,user_id,page_no,status, nice, selected, http_code from task_user_article WHERE selected = 0 and nice = 0 LIMIT %s"
    add_user_article_task = "replace into task_user_article(user_id,page_no,status, nice, selected, http_code , create_time ,update_time)value(%s,%s,0,0,0,-1,now(),now());"

    def __init__(self, setting):
        self.name = "task_user_article"
        self.primary_key = "task_id"
        BaseService.__init__(self, self.name, self.get_task_sql, self.name, self.primary_key, UserArticle, setting)

    def if_has_data(self, content):
        if content:
            try:
                i = content.index('count')
                return True
            except:
                pass
        return False

    def parse_content(self, content, link_job):
        task = link_job.task
        user_id = task.uid
        page_no = task.no
        data = json.loads(content)
        max_page = data['maxPage']
        mysql_util_instance = MysqlUtil()
        if max_page > 1:
            for i in range(2, max_page + 1):
                sql = self.add_user_article_task % (user_id, i)
                mysql_util_instance.execute(sql)
        mysql_util_instance.close()
        statuses = data['statuses']
        for item in statuses:
            id = item['id']
            count = MongoUtil.count('xq_user_article', {"id": id})
            if count == 0:
                MongoUtil.insert('xq_user_article', item)
