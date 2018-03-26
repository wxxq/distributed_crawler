#-*- coding: utf-8 -*-
import mycurl
import sys
import traceback
import logging as log
class BaseParseService(object):


    def __init__(self,setting):
        self.setting = setting

    def if_has_data(self,content):
        pass

    def parse_content(self,content,link_job):
        pass

    def check_proxy_available(self,ip, port):
        response=self.get_check_response(ip,port)
        flag = False
        if response.status == 200:
            flag = True
        return flag

    def get_check_response(self,ip, port):
        response = None
        try:
            response = mycurl.get(self.setting['check_url'],request_headers=self.setting['check_headers'],timeout=10, proxy="%s:%s" % (ip,port))
        except:
             t, v, tb = sys.exc_info()
             log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
        return response