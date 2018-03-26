#-*- coding: utf-8 -*-
from base_parse_service import BaseParseService
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import json
import traceback
from src.train.util.data_service import DataService
from src.train.job.station_task import TrainStop
import logging as log

class StationParseService(BaseParseService):

    def __init__(self,setting):
        BaseParseService.__init__(self,setting)

    def if_has_data(self,content):
        if content:
            try:
                json_obj = json.loads(content)
                if json_obj['data']:
                    return True
            except:
                pass
        return False

    def parse_content(self,content,link_job):
        json_obj = json.loads(content)
        data = json_obj['data']['data']
        typeName = data[0]['train_class_name']
        start_time = data[0]['start_time']
        pre_time = start_time
        duration = 0
        name_list = {}
        days = 0
        train_no = link_job.task.train_no
        # 保存站点数据
        for i,d in enumerate(data):
            arrive_time = d['arrive_time']
            depart_time = d['start_time']
            if i==0 :
                arrive_time = 'null'
            if i != 0:
                if self.compareSS(pre_time,arrive_time)<0:
                    days +=1
                duration = duration + self.getDaysSS(start_time,d['arrive_time'],days)
                pre_time = arrive_time
                if int(d['station_no'])==1:
                    raise  Exception
            stayTime = 0
            if i!=0 and i!= len(data)-1 :
                stayTime = d['stopover_time']
                try:
                    stayTime = stayTime[0:str(stayTime).index('分')]
                except Exception as e:
                    stayTime=0
                    # raise e
            if i == len(data)-1:
                depart_time = 'null'
            try:
                train_stop = TrainStop(link_job.task.train_code,d['station_name'],int(d['station_no']),arrive_time,stayTime,days,duration,depart_time,typeName,train_no)
                DataService.save_train_stop(train_stop)
                log.info("catch station:%s %s"%(link_job.task.train_code.decode("unicode-escape"),d['station_name'].decode("unicode-escape")))
                name_list.update({d['station_no']:d['station_name']})
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
        # 保存站到站
        kvs = name_list.items()
        i = -1
        for ki,vi in kvs:
            i += 1
            j = -1
            for kj,vj in  kvs:
                j += 1
                if i == j:
                    continue
                start_station = vi
                end_station = vj
                try:
                    # start_py = DataService.get_alia_by_station(start_station)
                    # if start_py == '':
                    #     start_py =  py_util.hanzi2pinyin_split(string=start_station, split="", firstcode=False)
                    # end_py = DataService.get_alia_by_station(end_station)
                    # if end_py == '':
                    #     end_py =  py_util.hanzi2pinyin_split(string=end_station, split="", firstcode=False)
                    DataService.save_s2s(start_station,'',end_station,'')
                    log.info("station to station records:%s --> %s" %(start_station,end_station))
                except:
                    t, v, tb = sys.exc_info()
                    log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    def compareSS(self,start,end):
        s_min = str(start).split(':')
        e_min = str(end).split(':')
        s_int = int(s_min[0])*60+int(s_min[1])
        e_int = int(e_min[0])*60+int(e_min[1])
        duration = e_int-s_int
        return duration*60

    def getDaysSS(self,start,end,days):
        s_min = str(start).split(':')
        e_min = str(end).split(':')
        s_int = int(s_min[0])*60+int(s_min[1])
        e_int = int(e_min[0])*60+int(e_min[1])
        duration = 0
        if days == 0:
            duration = e_int-s_int
        else:
            duration = e_int+24*60-s_int
        return duration*60