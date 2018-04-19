# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.dp_task import DPListTask,DPShopTask

#点评商户
dp_shop_job = "select url_id,url,shop_id,city_id,category_id,status, nice, selected, http_code from dp_shop_url WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_dp_shop_selected = 'update dp_shop_url set selected =%s where url_id = %s'
upt_dp_shop_task = "update dp_shop_url set status=%s,nice=%s,selected =%s,http_code=%s where url_id =%s"

#点评列表
DP_LIST_JOB ="select id,url,status, nice, selected, http_code from dp_list_url WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_dp_list_selected = 'update dp_list_url set selected =%s where id = %s'
upt_dp_list_task = "update dp_list_url set status=%s,nice=%s,selected =%s,http_code=%s where id =%s"


class DPShopService(BaseService):

    def __init__(self,setting):
        BaseService.__init__(self,dp_shop_job,upt_dp_shop_selected,upt_dp_shop_task,DPShopTask,setting)


class DPListService(BaseService):

    def __init__(self,setting):
        BaseService.__init__(self,DP_LIST_JOB,upt_dp_shop_selected,upt_dp_shop_task,DPShopTask,setting)
