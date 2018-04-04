# -*- coding: utf-8 -*-
import time

class LinkJob(object):
    
    def __init__(self, task):
        self.task_id = task.task_id
        self.url = task.url
        self.tick_time = time.time()
        self.http_code =task.http_code
        self.status = task.status
        self.nice = task.nice
        self.fetched_date = task.fetched_date
        self.task = task
    
    def __cmp__(self, link_job):
        if isinstance(link_job, LinkJob):
            return cmp(self.tick_time, link_job.tick_time)
        else:
            return -1


class Userjob(object):

    def __init__(self,user):
        self.tick_time = time.time()
        self._id = user["_id"]
        self.id = user["id"]
        self.level = user["level"]
        self.url = self._create_url()


    def _create_url(self):
        url ="https://xueqiu.com/friendships/followers.json?uid=%s&pageNo=1" % self.id
        return url

    def __cmp__(self, user_job):
        if isinstance(user_job, Userjob):
            return cmp(self.tick_time, user_job.tick_time)
        else:
            return -1

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key,value)

    def to_str(self):
        return "%s,%s,%s" % (self._id,self.id,self.level)

if __name__ == '__main__':
    import os