# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
from mysql_util import DataBaseUtil
from job.link_job import LinkJob
from job.station_task import StationTask
from job.dp_task import DPListTask,DPShopTask
#代理Sql
sql_proxy = 'select id,ip,port from train_proxy where is_use=0 group by ip'
update_proxy_state = 'update train_proxy set is_use =1 where id = %s'
update_proxys = 'update train_proxy set is_use =1 where is_use =0'
#任务sql
sql_job = 'SELECT id, begin_stop, ctrip_begin_stop, end_stop, ctrip_end_stop, status, nice, selected, fetched_date, http_code from station_task_tc WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s'
update_selected = 'update station_task_tc set selected =%s where id = %s'
update_task = "update station_task_tc set status=%s,nice=%s,selected =%s,fetched_date='%s',http_code=%s where id =%s"

find_station_sql = "select `id`, `train_code`, `name`, `sequence`, `arrive_time`, `staytime`, `days`, `duration`, `depart_time`, `grade`, `train_no` from train_line_stop_tc where train_code ='%s' and name ='%s'"
check_train_code_exist = "select count(*) from train_line_stop_tc where train_code ='%s'"
insert_price_sql = "replace into train_price_tc(train_code,name,from_name,start_time,end_time,duration,hard_seat,soft_seat,hard_bed_1,soft_bed_1,class_1,class_2,high_grade_bed_2,business_seat,grade,days,premium_seat,origin_stop,terminal,sequence,train_no,staytime,is_correct,state,notes) values('%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,'%s','%s',%s,'%s',%s,%s,%s,'%s')"

train_code_sql = "SELECT id, start_station,end_station,train_no,train_code, status, nice, selected, fetched_date, http_code from train_task WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT 500"
get_abbreviation_sql = "select abbreviation from station_name_12306 where station_name = '%s'"
update_train_state = "update train_task set selected =%s where id = %s"
update_train_task = "update train_task set status=%s,nice=%s,selected =%s,fetched_date='%s',http_code=%s where id =%s"

ist_stop_sql = "replace into train_line_stop_tc(train_code,name,sequence,arrive_time,staytime,days,duration,depart_time,grade,train_no)value('%s','%s',%s,'%s',%s,%s,%s,'%s','%s','%s')"
get_alia_station = "select quanpin from station_name_tc where name = '%s'"
insert_s2s = "replace INTO `station_task_tc` (`begin_stop`, `ctrip_begin_stop`, `end_stop`, `ctrip_end_stop`, `status`, `nice`, `selected`, `fetched_date`, `http_code`) VALUES ( '%s', '%s', '%s', '%s', '0', '0', '0', '', -1);"

sql_stop_no = "SELECT train_code,train_no from train_line_stop_tc GROUP BY train_code"
insert_merge_stop = "REPLACE INTO train_code_merge (train_code,train_no,substring_str) values('%s','%s','%s')"
update_merge_stop = "UPDATE train_code_merge set merger_code = '%s' where substring_str = '%s'"
merge_codes =  "SELECT train_code,merger_code from train_code_merge where  LOCATE('/',merger_code)!=0"
get_stops = "select * from train_line_stop_tc where train_code ='%s'"
update_price_code = "update train_price_tc set train_code = '%s' where train_code = '%s'"

# 点评列表
ist_dp_shop = "replace INTO `dianping`.`dp_shop_url` (`url`, `shop_id`, `city_id`, `category_id`, `province_id`, `create_time`, `nice`, `selected`, `status`, `http_code`) VALUES ('%s', %s, %s, %s,NULL, now(), 0, 0, 0, '-1')"


class DataService(object):

    def __init__(self):
        pass

    @classmethod
    def get_train_code_list(cls):
        train_code_list = DataBaseUtil.select(train_code_sql)
        return train_code_list

    @classmethod
    def get_abbreviation(cls,station_name):
        abbreviation = DataBaseUtil.select(get_abbreviation_sql%station_name)
        if len(abbreviation) == 0:
            return ''
        else:
            abbreviation = abbreviation[0][0]
            return abbreviation


    @classmethod
    def select_proxy(cls):
        proxys = DataBaseUtil.select(sql_proxy)
        return proxys

    @classmethod
    def update_proxy_state(cls,id):
        DataBaseUtil.execute(update_proxy_state % id)

    @classmethod
    def update_proxys(cls):
        DataBaseUtil.execute(update_proxys)




    @classmethod
    def update_task_selected(cls,state,id):
        DataBaseUtil.execute(update_selected%(state,id))


    @classmethod
    def update_task(cls,status,nice,selected,fetched_date,http_code,task_id):
        DataBaseUtil.execute(update_task %(status,nice,selected,fetched_date,http_code,task_id))

    @classmethod
    def update_train_task(cls,status,nice,selected,fetched_date,http_code,task_id):
        DataBaseUtil.execute(update_train_task %(status,nice,selected,fetched_date,http_code,task_id))

    @classmethod
    def find_station(cls,train_code,name):
        trains = DataBaseUtil.select(find_station_sql %(train_code,name) )
        return trains


    @classmethod
    def check_traincode_exist(cls,train_code):
        count = DataBaseUtil.select(check_train_code_exist%train_code )[0][0]
        if count == 0:
            return False
        else:
            return True

    @classmethod
    def save_train_price(cls,price):
        price_sql = insert_price_sql % (price.train_code ,price.end_station,price.start_station,price.depart_time,price.arrive_time,price.duration,price.A1,price.A2,price.A3,price.A4,price.M,price.O,price.A6,price.A9,price.grade,price.days,price.P,price.origin,price.terminal,price.sequence,price.train_no,price.stayTime,price.is_correct,price.state,price.note)
        DataBaseUtil.execute(price_sql)

    @classmethod
    def save_train_stop(cls,train_stop):
        DataBaseUtil.execute(ist_stop_sql % (train_stop.train_code,train_stop.station_name,train_stop.station_no,train_stop.arrive_time,train_stop.stayTime,train_stop.days,train_stop.duration,train_stop.depart_time,train_stop.typeName,train_stop.train_no))

    @classmethod
    def get_alia_by_station(cls,station_name):
        pinyin = DataBaseUtil.select(get_alia_station%station_name)
        if len(pinyin) == 0:
            return ''
        else:
            abbreviation = pinyin[0][0]
            return abbreviation

    @classmethod
    def save_s2s(cls,start_station,s_alia,end_station,e_alia):
         DataBaseUtil.execute(insert_s2s%(start_station,s_alia,end_station,e_alia))

    @classmethod
    def get_stop_no(cls):
        data = DataBaseUtil.select(sql_stop_no)
        return data

    @classmethod
    def insert_merge_stop(cls,train_code,train_no,substring_str):
        DataBaseUtil.execute(insert_merge_stop %(train_code,train_no,substring_str))

    @classmethod
    def update_merge_stop(cls,merger_code,substring_str):
        DataBaseUtil.execute(update_merge_stop%(merger_code,substring_str))

    @classmethod
    def select_merge_codes(cls):
        data = DataBaseUtil.select(merge_codes)
        return data

    @classmethod
    def get_stops(cls,train_code):
        data = DataBaseUtil.select(get_stops % train_code)
        return data

    @classmethod
    def update_price_code(cls,merge_code,train_code):
        DataBaseUtil.execute(update_price_code % (merge_code,train_code))

    @classmethod
    def save_dp_shop(cls,url,shop_id,city_id,category_id):
        DataBaseUtil.execute(ist_dp_shop %(url,shop_id,city_id,category_id))

