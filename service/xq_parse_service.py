#-*- coding: utf-8 -*-
import json
import sys
import traceback
import logging as log
from base_parse_service import BaseParseService
from util.mongo_util import MongoUtil

class XQParseService(BaseParseService):

    def __init__(self,setting):
        BaseParseService.__init__(self,setting)

    def if_has_data(self,content):
        if content:
            try:
                i = content.index('anonymous_count')
                return True
            except:
                pass
        return False

    def parse_content(self,content,link_job):
        task = link_job.task
        user_id = task.uid
        page_no = task.no
        level = task.level
        data=json.loads(content)
        followers = data["followers"]
        for follower in followers:
            id = follower["id"]
            count = MongoUtil.count("xq_user", {"id": id})
            if count == 0:
                follower["level"] = level + 1
                MongoUtil.insert("xq_user", follower)

    def parse_content_to_file(self,content,link_job):
        task = link_job.task
        user_id = task.uid
        page_no = task.no
        file_name = self.setting['store_path'] %(user_id,page_no)
        try:
            with open(file_name,'w') as f:
                f.write(content)
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    def check_proxy_available(self,ip, port):
        flag = False
        response=self.get_check_response(ip,port)
        if response and response.status ==200:
            try:
                i=response.body.index('雪球')
                flag = True
            except:
                pass
        return flag