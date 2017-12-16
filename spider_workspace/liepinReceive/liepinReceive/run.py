#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scrapy import cmdline
# cmdline.execute("scrapy crawl liepin".split())
# # cmdline.execute("scrapy crawl dazhong -s JOBDIR=crawls/dazhong-1".split())
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    while True:
        try:
            os.system("scrapy crawl liepin")
        except:
            pass