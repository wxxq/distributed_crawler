# -*- coding:utf-8 -*-
import sys
from src.train.service.base_service import BaseService
from src.train.job.dp_task import DPListTask,DPShopTask

#点评
dp_shop_job = "select url_id,url,shop_id,city_id,category_id,status, nice, selected, http_code from dp_shop_url WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_dp_shop_selected = 'update dp_shop_url set selected =%s where url_id = %s'
upt_dp_shop_task = "update dp_shop_url set status=%s,nice=%s,selected =%s,http_code=%s where url_id =%s"

class DPService(BaseService):

    def __init__(self):
        BaseService.__init__(self,dp_shop_job,upt_dp_shop_selected,upt_dp_shop_task,DPShopTask)

