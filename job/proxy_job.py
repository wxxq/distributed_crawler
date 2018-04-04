# -*- coding: utf-8 -*-
import time


class ProxyJob(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tick_time = time.time()

    def __cmp__(self, proxy_job):
        if isinstance(proxy_job, ProxyJob):
            return cmp(self.tick_time, proxy_job.tick_time)
        else:
            return -1


class T(object):
    dd = 0

    def __init__(self):
        pass


if __name__ == '__main__':
    a = T()
    b = T()
    a.dd +=1
    print b.dd

