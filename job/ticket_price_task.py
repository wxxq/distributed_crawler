# -*- coding:utf-8 -*-
import time
import json
from base_task import BaseTask


class TicketPriceTask(BaseTask):


    def __init__(self,task_id,begin_stop,ctrip_begin_stop,end_stop,ctrip_end_stop,status,nice,selected,fetched_date,http_code):
        self.begin_stop = begin_stop
        self.ctrip_begin_stop = ctrip_begin_stop
        self.end_stop = end_stop
        self.ctrip_end_stop = ctrip_end_stop
        BaseTask.__init__(self,task_id,status,nice,selected,http_code,fetched_date)
        self.url = self.__create_url()


    def __create_url(self):
        millis = int(round(time.time() * 1000))
        callback = "jQuery18309102298273607763_%s" % millis
        para ={"To":self.end_stop,"From":self.begin_stop,"TrainDate":self.fetched_date,"PassType":"","TrainClass":"","FromTimeSlot":"","ToTimeSlot":"","FromStation":"","ToStation":"","SortBy":"fromTime","callback":"","tag":"","memberId":"0","headct":"0","platId":1,"headver":"1.0.0","headtime":int(round(time.time() * 1000))}
        para=json.dumps(para)
        url = "https://www.ly.com/uniontrain/trainapi/TrainPCCommon/SearchTrainRemainderTickets?callback=%s&para=%s"
        url = url % (callback,para)
        return url

class Price(object):
    def __init__(self,train_code,end_station,start_station,depart_time,arrive_time,duration,A1,A2,A3,A4,O,M,A6,A9,grade,days,P,origin,terminal,sequence,train_no,stayTime,is_correct,state,note):
        self.train_code = train_code
        self.end_station = end_station
        self.start_station = start_station
        self.depart_time = depart_time
        self.arrive_time = arrive_time
        self.duration = duration
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.O = O
        self.M = M
        self.A6 = A6
        self.A9 = A9
        self.grade = grade
        self.days = days
        self.P = P
        self.origin = origin
        self.terminal = terminal
        self.sequence = sequence
        self.train_no = train_no
        self.stayTime = stayTime
        self.is_correct = is_correct
        self.state =  state
        self.note = note

if __name__ == '__main__':
    task = TicketPriceTask(1,'北京','','上海','',1,1,1,'2017-07-14',1)
    print task.url