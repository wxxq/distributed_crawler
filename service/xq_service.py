# -*- coding:utf-8 -*-
import sys
from src.train.service.base_service import BaseService
from src.train.job.xq_user_task import User

#雪球
get_task_sql = "select task_id,user_id,page_no,status, nice, selected, http_code from task_user WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"
upt_xq_task_selected = "update task_user set selected =%s where task_id = %s"
upt_xq_task = "update task_user set status=%s,nice=%s,selected =%s,http_code=%s where task_id =%s"

class XQService(BaseService):

    def __init__(self,setting):
        BaseService.__init__(self,get_task_sql,upt_xq_task_selected,upt_xq_task,User,setting)

