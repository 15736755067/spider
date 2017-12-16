#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scrapy import cmdline
# cmdline.execute("scrapy crawl sofang".split())
# # cmdline.execute("scrapy crawl guangchang -s JOBDIR=crawls/guangchang-1".split())
import time
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    file_name = os.path.dirname(__file__) + '/' + 'ok.txt'
    print file_name
    i = 0
    while True:
        time.sleep(5)
        try:
            if i == 0:
                i = 1
                os.system("scrapy crawl sofang")
            else:
                time.sleep(5)
                ret = os.path.exists(file_name)
                if ret:
                    os.remove(file_name)
                    time.sleep(5)
                    os.system("scrapy crawl sofang")
        except:
            pass