#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import cmdline
while True:
    cmdline.execute("scrapy crawl guangchang".split())
# cmdline.execute("scrapy crawl guangchang -s JOBDIR=crawls/guangchang-1".split())