# -*- coding:utf-8 -*-
from base_task import BaseTask

class DPListTask(BaseTask):
    def __init__(self,task_id,url,status,nice,selected,http_code):
        self.url = url
        BaseTask.__init__(self,task_id,status,nice,selected,http_code,'2017-05-19')


class DPShopTask(BaseTask):
    def __init__(self,url_id,url,shop_id,city_id,category_id,status, nice, selected, http_code):
        self.url = url
        self.shop_id = shop_id
        self.city_id = city_id
        self.category_id = category_id
        BaseTask.__init__(self,url_id,status,nice,selected,http_code,'2017-05-19')