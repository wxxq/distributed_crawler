# -*- coding: utf-8 -*-
import json
import sys
import traceback
import logging as log
from base_parse_service import BaseParseService
from util.mongo_util import MongoUtil
from util.mysql_util import DataBaseUtil


class XQUserArticleParseService(BaseParseService):

    add_user_article_task = "replace into task_user_article(user_id,page_no,status, nice, selected, http_code , create_time ,update_time)value(%s,%s,0,0,0,-1,now(),now());"

    def __init__(self, setting):
        BaseParseService.__init__(self, setting)

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
        data=json.loads(content)
        max_page=data['maxPage']
        if max_page > 1:
            for i in range(2,max_page+1):
                sql=self.add_user_article_task % (user_id,i)
                DataBaseUtil.execute(sql)
        statuses = data['statuses']
        for item in statuses:
            id = item['id']
            count = MongoUtil.count('xq_user_article',{"id":id})
            if count == 0:
                MongoUtil.insert('xq_user_article',item)


    def check_proxy_available(self, ip, port):
        flag = False
        response = self.get_check_response(ip, port)
        if response and response.status == 200:
            try:
                flag = True
            except:
                pass
        return flag
