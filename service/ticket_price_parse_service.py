#-*- coding: utf-8 -*-
from base_parse_service import BaseParseService
import sys
sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import json
from src.train.util.data_service import DataService
from src.train.job.ticket_price_task import Price
import traceback
import logging as log
import mycurl
import time
import datetime


class TicketPriceParseService(BaseParseService):

    def __init__(self,setting):
        BaseParseService.__init__(self,setting)

    def if_has_data(self,content):
        if content:
            try:
                content = content[content.index('(')+1:content.rindex(')')]
                json_obj = json.loads(content)
                if len(json_obj['data']["trains"]) != 0:
                    return True
            except:
                pass
        return False

    def parse_content(self,content,link_job):
        content = content[content.index('(')+1:content.rindex(')')]
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
                duration = int(train['usedTimeInt'])*60
                note = train['note']
                A1 = self.get_price('hardseat',train['ticketState'])
                A2 = self.get_price('softseat',train['ticketState'])
                A3 = self.get_price('hardsleepermid',train['ticketState'])
                A4 = self.get_price('softsleeperdown',train['ticketState'])
                A6 = self.get_price('advancedsoftsleeper',train['ticketState'])
                A9 = self.get_price('businessseat',train['ticketState'])
                O = self.get_price('secondseat',train['ticketState'])
                M = self.get_price('firstseat',train['ticketState'])
                P = self.get_price('specialseat',train['ticketState'])
                sequence = 0
                days = 0
                stayTime = 0
                grade = ''
                state = 0
                train_no = ''
                exist = DataService.check_traincode_exist(train_code)
                # is_correct 0：错误信息 1:正确
                is_correct = 1
                if len(train['ticketState']) ==0:
                    is_correct = 0
                #  state 0：正常   1：未收录此车次    2:收录此车次但是此站点已经取消
                if not exist:
                    state =1
                else:
                    station_s = DataService.find_station(train_code,start_station)
                    station_e = DataService.find_station(train_code,end_station)
                    if len(station_e) != 0 and len(station_s)!=0:
                        days_s = int(station_s[0][6])
                        if self.compareSS(station_s[0][4],station_s[0][8])<0:
                            days_s += 1
                        sequence = station_e[0][3]
                        days = station_e[0][6] - days_s
                        stayTime = station_e[0][5]
                        grade = station_e[0][9]
                        train_no = station_e[0][10]
                    else:
                        state =2
                price = Price(train_code,end_station,start_station,depart_time,arrive_time,duration,A1,A2,A3,A4,O,M,A6,A9,grade,days,P,origin,terminal,sequence,train_no,stayTime,is_correct,state,note)
                DataService.save_train_price(price)
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))

    def check_proxy_available(self,ip, port):
        flag = False
        try:
            detail = {"end_stop":"广州","begin_stop":"哈尔滨东","fetched_date":"2017-07-14"}
            check_url = self.create_url(detail)
            response = mycurl.get(check_url,request_headers=self.setting['CHECK_HEADERS'],timeout=5, proxy="%s:%s" % (ip,port))
            if response.status == 200:
                content = response.body
                if content:
                    content = content[content.index('(')+1:content.rindex(')')]
                    json_obj = json.loads(content)
                    if json_obj["status"]==200:
                        flag = True
        except:
            pass
        return flag

    def get_price(self,key,dic):
        p = 0
        if  len(dic)==0:
            return p
        if key in dic:
            p = dic[key]['price']
        return p

    def create_url(self,detail):
        millis = int(round(time.time() * 1000))
        callback = "jQuery18309102298273607763_%s" % millis
        para ={"To":detail['end_stop'],"From":detail['begin_stop'],"TrainDate":detail['fetched_date'],"PassType":"","TrainClass":"","FromTimeSlot":"","ToTimeSlot":"","FromStation":"","ToStation":"","SortBy":"fromTime","callback":"","tag":"","memberId":"0","headct":"0","platId":1,"headver":"1.0.0","headtime":int(round(time.time() * 1000))}
        para=json.dumps(para)
        url = "https://www.ly.com/uniontrain/trainapi/TrainPCCommon/SearchTrainRemainderTickets?callback=%s&para=%s"
        url = url % (callback,para)
        return url

    def increaseDate(self,dateStr,day=1):
        try:
            d = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
            delta=datetime.timedelta(days=day)
            n_days=d+delta
            tDate = n_days.strftime('%Y-%m-%d')
            return tDate
        except Exception ,e:
            print e
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def compareSS(self,start,end):
        if start is None:
            start = "0:0"
        if end is None:
            end = "0:0"
        s_min = str(start).split(':')
        e_min = str(end).split(':')
        s_int = int(s_min[0])*60+int(s_min[1])
        e_int = int(e_min[0])*60+int(e_min[1])
        duration = e_int-s_int
        return duration*60