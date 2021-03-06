# -*- coding:utf-8  -*-
import sys
import traceback

sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import MySQLdb
# from DBUtils.PooledDB import PooledDB
from settings import database
import logging as log
import time


class DataBaseUtil(object):
    def __init__(self):
        self.host = database['host']
        self.user = database['user']
        self.passwd = database['passwd']
        self.db = database['db']

    @classmethod
    def getConn(cls):
        conn = None
        is_false = True
        while is_false:
            try:
                conn = MySQLdb.connect(db=database['db'], host=database['host'], user=database['user'],
                                       passwd=database['passwd'], charset='utf8')
                is_false = False
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
                time.sleep(0.5)
        return conn

    @classmethod
    def execute(cls, sql):
        log.debug(sql)
        conn = cls.getConn()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    @classmethod
    def select(cls, sql):
        conn = cls.getConn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return result


class MysqlUtil(object):
    def __init__(self):
        self.host = database['host']
        self.user = database['user']
        self.passwd = database['passwd']
        self.db = database['db']
        self.conn = self.getConn()

    def getConn(self):
        conn = None
        is_false = True
        while is_false:
            try:
                conn = MySQLdb.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd, charset='utf8')
                is_false = False
            except:
                t, v, tb = sys.exc_info()
                log.error("%s,%s,%s" % (t, v, traceback.format_tb(tb)))
                time.sleep(0.5)
        return conn

    def execute(self, sql):
        log.debug(sql)
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    print 'start init '
