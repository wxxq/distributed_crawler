# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.dp_task import DPListTask, DPShopTask
import logging as log
import traceback
import json
from util.data_service import DataService

# 点评商户
dp_shop_job = "select url_id,url,shop_id,city_id,category_id,status, nice, selected, http_code from dp_shop_url WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_dp_shop_selected = 'update dp_shop_url set selected =%s where url_id = %s'
upt_dp_shop_task = "update dp_shop_url set status=%s,nice=%s,selected =%s,http_code=%s where url_id =%s"

# 点评列表
DP_LIST_JOB = "select id,url,status, nice, selected, http_code from dp_list_url WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_dp_list_selected = 'update dp_list_url set selected =%s where id = %s'
upt_dp_list_task = "update dp_list_url set status=%s,nice=%s,selected =%s,http_code=%s where id =%s"


class DPShopService(BaseService):
    shop_url_pattern = "http://www.dianping.com/shop/%s"

    def __init__(self, setting):
        BaseService.__init__(self, dp_shop_job, upt_dp_shop_selected, upt_dp_shop_task, DPShopTask, setting)

    def if_has_data(self, content):
        if content:
            try:
                i = content.index('大众点评网')
                return True
            except:
                pass
        return False

    def parse_content(self, content, link_job):
        task = link_job.task
        city_id = task.city_id
        shop_id = task.shop_id
        category_id = task.category_id
        file_name = 'E:/Train/src/files/%s-%s-%s.html' % (shop_id, city_id, category_id)
        try:
            with open(file_name, 'w') as f:
                f.write(content)
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))


class DPListService(BaseService):

    shop_url_pattern = "http://www.dianping.com/shop/%s"

    def __init__(self, setting):
        BaseService.__init__(self, DP_LIST_JOB, upt_dp_shop_selected, upt_dp_shop_task, DPShopTask, setting)

    def if_has_data(self, content):
        if content:
            try:
                json_obj = json.loads(content)
                if len(json_obj["list"]) != 0:
                    return True
            except:
                pass
        return False

    def parse_content(self, content, link_job):
        json_obj = json.loads(content)
        list = json_obj['list']
        for shop in list:
            try:
                category_id = shop['categoryId']
                city_id = shop['cityId']
                shop_id = shop['id']
                url = self.shop_url_pattern % shop_id
                DataService.save_dp_shop(url, shop_id, city_id, category_id)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
