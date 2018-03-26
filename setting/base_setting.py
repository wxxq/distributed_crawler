#-*- coding:utf-8 -*-

class BaseSetting(object):

    def __init__(self,obj):
        self.setting_wrapper = obj

    def __getitem__(self,key):
        return self.setting_wrapper[key]