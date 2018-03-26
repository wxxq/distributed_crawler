#-*- coding: utf-8 -*-
import sys
sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import json
import traceback
from data_service import DataService
from mysql_util import DataBaseUtil
from pinyin import PinYin
py_util = PinYin()
py_util.load_word('../word.data')
def main():
        # 保存站到站
        temp_trains = []
        for code in temp_trains:
            names = DataBaseUtil.select("select name from train_line_stop where train_code = '%s' order by sequence" % code)
            if len(names) >  0:
                key = 0
                name_list = {}
                for n in names:
                    name_list[key] = n[0]
                    key = key+1
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
                            start_py = DataService.get_alia_by_station(start_station)
                            if start_py == '':
                                start_py =  py_util.hanzi2pinyin_split(string=start_station, split="", firstcode=False)
                            end_py = DataService.get_alia_by_station(end_station)
                            if end_py == '':
                                end_py =  py_util.hanzi2pinyin_split(string=end_station, split="", firstcode=False)
                            DataService.save_s2s(start_station,start_py,end_station,end_py)
                        except:
                            t, v, tb = sys.exc_info()


if __name__ == '__main__':
    main()