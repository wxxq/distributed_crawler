# -*- coding:utf-8 -*-
import urllib2
import os
import requests
from StringIO import StringIO
import gzip
import re
import sys
sys.path.append("..")
import mycurl
def do_load_media(url, path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def load_media():
    url = 'https://dict.youdao.com/dictvoice?audio=%s&type=2'
    path = r'E:/LiDuoer/%s.mp3'
    english_words_file=open('test.txt')
    replace_char = r'[’？\.,\(\)\?（）\/]'
    for word in english_words_file.readlines():
        word=word.strip()
        print word
        file_name_string=re.sub(replace_char," ",word)
        word_arrays=file_name_string.split(" ")
        if len(word_arrays)>10:
            word_file_name = "_".join(word_arrays[0:10])
        else:
            word_file_name = "_".join(word_arrays)
        item_url = url % word
        item_path = path % word_file_name
        do_load_media(item_url, item_path)
    pass


def main():
    load_media()
    pass

def down(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'aliyungf_tc=AQAAAOhjwRDk7wEAqbEbd+AUjwN6S5dQ; xq_a_token=0d524219cf0dd2d0a4d48f15e36f37ef9ebcbee1; xq_a_token.sig=P0rdE1K6FJmvC2XfH5vucrIHsnw; xq_r_token=7095ce0c820e0a53c304a6ead234a6c6eca38488; xq_r_token.sig=xBQzKLc4EP4eZvezKxqxXNtB7K0; u=231524468913763; device_id=e24f3c89cceb3d13f617ecfcc0611357; s=fc14nz9vss; __utmt=1; __utma=1.1299756509.1521955892.1524127246.1524479246.33; __utmb=1.3.10.1524479246; __utmc=1; __utmz=1.1524479246.33.3.utmcsr=xueqiu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_1db88642e346389874251b5a1eded6e3=1524127245,1524468511,1524468798,1524468914; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1524479272',
        'Host':'xueqiu.com',
        'Upgrade-Insecure-Requests':'1',
        'X-Requested-With':'XMLHttpRequest'
    }
    proxies={"http":"1319.27.177.169:8088"}   #设置你想要使用的代理
    proxy_s=urllib2.ProxyHandler(proxies)
    opener=urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    content = f.read()
    print content

def check_proxy_available(url, ip, port):
        response, flag = None, False
        head = [
            "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ,"Accept-Encoding:gzip, deflate, sdch, br"
            ,"Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
            ,"Cache-Control:max-age=0"
            ,"Connection:keep-alive"
            ,"Cookie:aliyungf_tc=AQAAAOhjwRDk7wEAqbEbd+AUjwN6S5dQ; xq_a_token=0d524219cf0dd2d0a4d48f15e36f37ef9ebcbee1; xq_a_token.sig=P0rdE1K6FJmvC2XfH5vucrIHsnw; xq_r_token=7095ce0c820e0a53c304a6ead234a6c6eca38488; xq_r_token.sig=xBQzKLc4EP4eZvezKxqxXNtB7K0; u=231524468913763; device_id=e24f3c89cceb3d13f617ecfcc0611357; s=fc14nz9vss; __utmt=1; __utma=1.1299756509.1521955892.1524127246.1524479246.33; __utmb=1.4.10.1524479246; __utmc=1; __utmz=1.1524479246.33.3.utmcsr=xueqiu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_1db88642e346389874251b5a1eded6e3=1524127245,1524468511,1524468798,1524468914; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1524480882"
            ,"Host:xueqiu.com"
            ,"Upgrade-Insecure-Requests:1"
            ,"User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        ]
        response = mycurl.get(url, request_headers=head, timeout=10,
                                  proxy="%s:%s" % (ip, port))
        if response and response.status == 200:
            buf = StringIO( response.body)
            f = gzip.GzipFile(fileobj=buf)
            content = f.read()
            print content

if __name__ == '__main__':
    check_proxy_available("https://xueqiu.com/cubes/list.json?user_id=6569044359","119.27.177.169",80)
