#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from scrapy import cmdline
# cmdline.execute("scrapy crawl job51".split())
# cmdline.execute("sacrapy crawl zhi_lian -s JOBDIR=crawls/zhi_lian-1".split())
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    while True:
        try:
            os.system("scrapy crawl job51")
        except:
            pass