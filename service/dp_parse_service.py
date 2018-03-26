#-*- coding: utf-8 -*-
import json
import sys
import traceback
import logging as log
import mycurl
from base_parse_service import BaseParseService
from src.train.util.data_service import DataService


class DPShopParseService(BaseParseService):
    shop_url_pattern = "http://www.dianping.com/shop/%s"

    def __init__(self,setting):
        BaseParseService.__init__(self,setting)

    def if_has_data(self,content):
        if content:
            try:
                i = content.index('大众点评网')
                return True
            except:
                pass
        return False

    def parse_content(self,content,link_job):
        task = link_job.task
        city_id = task.city_id
        shop_id = task.shop_id
        category_id = task.category_id
        file_name = 'E:/Train/src/files/%s-%s-%s.html' %(shop_id,city_id,category_id)
        try:
            with open(file_name,'w') as f:
                f.write(content)
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    def check_proxy_available(self,ip, port):
        flag = False
        try:
            response = mycurl.get(self.setting['check_url'],request_headers=self.setting['check_heades'],timeout=10, proxy="%s:%s" % (ip,port))
            if response.status == 200:
                content = response.body
                if content == "OK":
                    flag = True
                # if content:
                #     i = content.index('大众点评网')
                #     flag = True
        except:
            pass
        return flag

class DPListParseService(BaseParseService):

    shop_url_pattern = "http://www.dianping.com/shop/%s"

    def __init__(self,setting):
        BaseParseService.__init__(self,setting)

    def if_has_data(self,content):
        if content:
            try:
                json_obj = json.loads(content)
                if len(json_obj["list"]) != 0:
                    return True
            except:
                pass
        return False

    def parse_content(self,content,link_job):
        json_obj = json.loads(content)
        list = json_obj['list']
        for shop in list:
            try:
                category_id = shop['categoryId']
                city_id = shop['cityId']
                shop_id = shop['id']
                url = self.shop_url_pattern %  shop_id
                DataService.save_dp_shop(url,shop_id,city_id,category_id)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    def check_proxy_available(self,ip, port):
        flag = False
        try:
            response = mycurl.get(self.setting['check_url'],request_headers=self.setting['check_headers'],timeout=5, proxy="%s:%s" % (ip,port))
            if response.status == 200:
                content = response.body
                if content:
                    json_obj = json.loads(content)
                    if json_obj["recordCount"]:
                        flag = True
        except:
            pass
        return flag