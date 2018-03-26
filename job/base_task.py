#-*- coding:utf-8 -*-

class BaseTask(object):

    def __init__(self,task_id,status,nice,selected,http_code,fetched_date):
        self.task_id = task_id
        self.status = status
        self.nice = nice
        self.selected = selected
        self.http_code = http_code
        self.fetched_date = fetched_date

    def __create_url(self):
        pass