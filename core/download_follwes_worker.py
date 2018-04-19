# -*- coding: utf-8 -*-
import pycurl
import random
import socket
import sys
import threading
import traceback
from copy import copy
import urllib
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import logging as log
from job.page_job import PageJob
from errors import HostResolvedError, TimeoutError
from settings import PC_USER_AGENTS_SUM, PC_USER_AGENTS, OK_CODE, NOT_FOUND
from StringIO import StringIO
import gzip
import urllib2
import json
from util.mongo_util import MongoUtil
from util.mysql_util import DataBaseUtil
from util.redis_util import RedisUtil
import os

HEAD = [
    "Accept:application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding:gzip, deflate, sdch, br",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Connection:keep-alive",
    "Host:xueqiu.com",
    "Referer:https://xueqiu.com/people",
    "Cookie:__utmz=1.1521950844.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); device_id=8147d889099b145fc775c0afa66ccf78; s=fz11cvq46z; aliyungf_tc=AQAAAOMxjC41uAYAQoXv26zn8nDN45rg; xq_a_token=229a3a53d49b5d0078125899e528279b0e54b5fe; xq_a_token.sig=oI-FfEMvVYbAuj7Ho7Z9mPjGjjI; xq_r_token=8a43eb9046efe1c0a8437476082dc9aac6db2626; xq_r_token.sig=Efl_JMfn071_BmxcpNvmjMmUP40; u=711522754903243; Hm_lvt_1db88642e346389874251b5a1eded6e3=1521950844,1522683252,1522685277,1522754903; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1522754903; __utma=1.1284817915.1521950844.1522683251.1522754903.3; __utmc=1; __utmt=",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]
IST_SQL = "replace into task_user(user_id,page_no,level,status, nice, selected, http_code)value(%s,%s,%s,0,0,0,-1);"

class DownloadFollowers(threading.Thread):
    """
        下载用户粉丝的第一页，确定用户粉丝数
    """

    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.dead_lock = threading.Lock()
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../persistence/parsed_mongo_id'))
        self.dead_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../persistence/dead_mongo_ids'))
        self.queue = crawler.user_check_queue
        if crawler.setting['if_use_proxy']:
            self.proxy_queue = crawler.proxy_queue

    def run(self):
        while True:
            user_job = self.queue.get()
            url = user_job.url
            status, content = self._down(url)
            if status == 200:
                self._parse(content,user_job)
            else:
                self._rw_dead_mongo_id(user_job)

    def _down(self, url):
        content = ''
        status = None
        response = None
        try:
            request_obj = urllib2.Request(url)
            for item in HEAD:
                key = item.split(":")[0]
                value = item.split(":")[1]
                request_obj.add_header(key, value)
            response = urllib2.urlopen(request_obj)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            response.close()
            status = response.code
        except Exception as e:
            t, v, tb = sys.exc_info()
            log.info("%s,%s,%s,%s" % (url, t, v, traceback.format_tb(tb)))

        if content and status:
            body_length = len(content)
        else:
            status, response, body_length = None, None, None
        log.info('Download url=%s, status=%s, response=%s, bodylength=%s, proxy=%s' % (
            url, status, response, body_length, 'none'))
        return status, content

    def _parse(self, content, user_job):
        data = json.loads(content)
        max_page = int(data["maxPage"])
        followers = data["followers"]
        level = user_job["level"] + 1
        for follower in followers:
            id = follower["id"]
            count = MongoUtil.count("xq_user", {"id": id})
            if count == 0:
                follower["level"] = level
                MongoUtil.insert("xq_user", follower)
        self._import_link_job(max_page,user_job)
        self._rw_parsed_mongo_id(self.path,"w",str(user_job["_id"]))
        RedisUtil.set(user_job["id"],1)


    def _import_link_job(self,max_page,user_job):
        if max_page > 1:
            user_id = user_job["id"]
            for i in range(2,max_page+1):
                sql=IST_SQL % (user_id,i,user_job["level"])
                DataBaseUtil.execute(sql)

    def _rw_parsed_mongo_id(self,path,model,content=""):
        with self.lock:
            f = open(path,model)
            return_content = None
            with f:
                if model == "r":
                    return_content=f.read()
                    return return_content
                elif model == "w":
                    f.write(content)

    def _rw_dead_mongo_id(self,user_job):
        with self.dead_lock:
            f=open(self.dead_path,"a")
            with f:
                f.write("%s\n"% user_job.to_str())