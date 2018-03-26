# -*- coding:utf-8 -*-
import sys
from base_task import BaseTask

URL_STATION = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s"


class StationTask(BaseTask):

    def __init__(self,start_station,end_station,train_no,useful_date,train_code,task_id,status,nice,selected,http_code):
        self.start_station = start_station
        self.end_station = end_station
        self.train_no = train_no
        self.train_code = train_code
        BaseTask.__init__(self,task_id,status,nice,selected,http_code,useful_date)
        self.url = self.__create_url()


    def __create_url(self):
        url = URL_STATION % (self.train_no,self.start_station,self.end_station,self.fetched_date)
        return url


class TrainStop(object):
    def __init__(self,train_code,station_name,station_no,arrive_time,stayTime,days,duration,depart_time,typeName,train_no):
        self.train_code = train_code
        self.station_name = station_name
        self.station_no = station_no
        self.arrive_time = arrive_time
        self.stayTime = stayTime
        self.days = days
        self.duration = duration
        self.depart_time =depart_time
        self.typeName = typeName
        self.train_no = train_no