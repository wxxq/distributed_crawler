# -*- coding:utf-8 -*-
import sys
from src.train.service.base_service import BaseService
from src.train.job.ticket_price_task import TicketPriceTask

sql_job = 'SELECT id, begin_stop, ctrip_begin_stop, end_stop, ctrip_end_stop, status, nice, selected, fetched_date, http_code from station_task_tc WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s'
update_selected = 'update station_task_tc set selected =%s where id = %s'
update_task = "update station_task_tc set status=%s,nice=%s,selected =%s,fetched_date='%s',http_code=%s where id =%s"

class TicketPriceService(BaseService):


    def __init__(self,setting):
        BaseService.__init__(self,sql_job,update_selected,update_task,TicketPriceTask,setting)
