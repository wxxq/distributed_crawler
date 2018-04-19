# -*- coding:utf-8 -*-
import urllib2
import os
import requests
import re
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
    headers = { 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
    proxies={"http":"60.12.126.150:8080"}   #设置你想要使用的代理
    proxy_s=urllib2.ProxyHandler(proxies)
    opener=urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    print response.read()

if __name__ == '__main__':
    # main()
    upt_task_selected = "update %s(table_name) set selected =%%s where task_id = %%s"
    print upt_task_selected % 'tt'
