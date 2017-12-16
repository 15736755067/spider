#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import cmdline
cmdline.execute("scrapy crawl tianxia".split())
# cmdline.execute("scrapy crawl guangchang -s JOBDIR=crawls/guangchang-1".split())