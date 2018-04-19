#-*- coding:utf-8 -*-
import sys
default_encoding = "utf-8"
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from settings import mongo_database
from pymongo import MongoClient
import logging as log
import time
import traceback

HOST = mongo_database['host']
PORT = mongo_database['port']
DB_NAME = mongo_database['db']
CONNECT = None

def connect():
    is_success = False
    while not is_success:
        try:
            global CONNECT
            CONNECT =MongoClient(HOST,PORT)
            is_success = True
        except:
            t, v, tb = sys.exc_info()
            log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
            time.sleep(0.5)

connect()
DB = CONNECT.__getitem__(DB_NAME)

class MongoUtil(object):

    def __init__(self):
        pass


    @classmethod
    def find(cls,collection,filter,searched_fields,batch_size=None):
        collection=DB.__getitem__(collection)
        if batch_size:
            cursor=collection.find(filter,searched_fields).sort([("_id",1)]).limit(batch_size)
        else:
            cursor=collection.find(filter,searched_fields).sort([("_id",1)])
        return cursor

    @classmethod
    def find_first_id(cls,collection,filter,searched_fields):
        collection=DB.__getitem__(collection)
        cursor=collection.find(filter,searched_fields).sort([("_id",1)]).limit(1)
        id = 0
        for document in cursor:
            id = document['_id']
        return str(id)

    @classmethod
    def insert(cls,collection,document):
        rtn=DB.__getitem__(collection).insert(document)
        return rtn

    @classmethod
    def count(cls,collection,filter):
        count=DB.__getitem__(collection).count(filter)
        return count

    @classmethod
    def delete(cls,collection,filter):
        DB.__getitem__(collection).delete_one(filter)

    @classmethod
    def close(self):
        CONNECT.close()


if __name__ == '__main__':
    from bson.objectid import ObjectId
    dict={}
    cursor = MongoUtil.find("xq_user",{},{"_id":1,"id":1})
    for item in cursor:
        id=item["id"]
        _id = item["_id"]
        exist = 0
        try:
            exist=dict[id]
        except:
            pass
        if not exist:
            dict[id] = 1
        else:
            print item
            MongoUtil.delete("xq_user",{"_id":ObjectId(_id)})
