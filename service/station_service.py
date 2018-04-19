# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.station_task import StationTask

#12306 站到站
train_code_sql = "SELECT id, start_station,end_station,train_no,train_code, status, nice, selected, fetched_date, http_code from train_task WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT 500"
update_train_state = "update train_task set selected =%s where id = %s"
update_train_task = "update train_task set status=%s,nice=%s,selected =%s,fetched_date='%s',http_code=%s where id =%s"


class StationService(BaseService):


    def __init__(self,setting):
        BaseService.__init__(self,train_code_sql,update_train_state,update_train_task,StationTask,setting)
