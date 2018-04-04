#-*- coding:utf-8 -*-

import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from yaml import load

def load_config(file_name):
    config_path = os.path.join(os.path.dirname(__file__), 'config/%s.yaml'% file_name)
    with open(config_path,'rb') as f:
        cont = f.read()
        cf = load(cont)
        return cf

if __name__ == '__main__':
    ticket_price_config=load_config('ticket_price')
    print ticket_price_config['proxy_frequency_time']
