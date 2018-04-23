# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.ticket_price_task import TicketPriceTask
import json
from util.data_service import DataService
from job.ticket_price_task import Price
import traceback
import logging as log
import mycurl
import time
import datetime

sql_job = 'SELECT id, begin_stop, ctrip_begin_stop, end_stop, ctrip_end_stop, status, nice, selected, fetched_date, http_code from station_task_tc WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s'
update_selected = 'update station_task_tc set selected =%s where id = %s'
update_task = "update station_task_tc set status=%s,nice=%s,selected =%s,fetched_date='%s',http_code=%s where id =%s"


class TicketPriceService(BaseService):
    def __init__(self, setting):
        BaseService.__init__(self, sql_job, update_selected, update_task, TicketPriceTask, setting)

    def if_has_data(self, content):
        if content:
            try:
                content = content[content.index('(') + 1:content.rindex(')')]
                json_obj = json.loads(content)
                if len(json_obj['data']["trains"]) != 0:
                    return True
            except:
                pass
        return False

    def parse_content(self, content, link_job):
        content = content[content.index('(') + 1:content.rindex(')')]
        json_obj = json.loads(content)
        trains = json_obj['data']['trains']
        for train in trains:
            try:
                train_code = train['trainNum']
                start_station = train['fromCity']
                end_station = train['toCity']
                origin = train['beginPlace']
                terminal = train['endPlace']
                depart_time = train['fromTime']
                arrive_time = train['toTime']
                duration = int(train['usedTimeInt']) * 60
                note = train['note']
                A1 = self.get_price('hardseat', train['ticketState'])
                A2 = self.get_price('softseat', train['ticketState'])
                A3 = self.get_price('hardsleepermid', train['ticketState'])
                A4 = self.get_price('softsleeperdown', train['ticketState'])
                A6 = self.get_price('advancedsoftsleeper', train['ticketState'])
                A9 = self.get_price('businessseat', train['ticketState'])
                O = self.get_price('secondseat', train['ticketState'])
                M = self.get_price('firstseat', train['ticketState'])
                P = self.get_price('specialseat', train['ticketState'])
                sequence = 0
                days = 0
                stayTime = 0
                grade = ''
                state = 0
                train_no = ''
                exist = DataService.check_traincode_exist(train_code)
                # is_correct 0：错误信息 1:正确
                is_correct = 1
                if len(train['ticketState']) == 0:
                    is_correct = 0
                # state 0：正常   1：未收录此车次    2:收录此车次但是此站点已经取消
                if not exist:
                    state = 1
                else:
                    station_s = DataService.find_station(train_code, start_station)
                    station_e = DataService.find_station(train_code, end_station)
                    if len(station_e) != 0 and len(station_s) != 0:
                        days_s = int(station_s[0][6])
                        if self.compareSS(station_s[0][4], station_s[0][8]) < 0:
                            days_s += 1
                        sequence = station_e[0][3]
                        days = station_e[0][6] - days_s
                        stayTime = station_e[0][5]
                        grade = station_e[0][9]
                        train_no = station_e[0][10]
                    else:
                        state = 2
                price = Price(train_code, end_station, start_station, depart_time, arrive_time, duration, A1, A2, A3,
                              A4, O, M, A6, A9, grade, days, P, origin, terminal, sequence, train_no, stayTime,
                              is_correct, state, note)
                DataService.save_train_price(price)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
