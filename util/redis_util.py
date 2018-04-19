#-*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import redis
from settings import redis_db
import logging as log
import time
import traceback


HOST = redis_db['host']
PORT = redis_db['port']
CONNECT = None
def connect():
    is_success = False
    while not is_success:
        try:
            global CONNECT
            CONNECT = redis.StrictRedis(HOST,PORT,password=123456)
            is_success = True
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
            time.sleep(0.5)

connect()

class RedisUtil(object):


    def __init__(self):
        pass

    @classmethod
    def get(self,key):
        if CONNECT.exists(key):
            return CONNECT.get(key)
        else:
            return False

    @classmethod
    def set(self,key,val):
        CONNECT.set(key,val)

