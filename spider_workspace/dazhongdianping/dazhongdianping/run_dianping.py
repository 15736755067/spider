#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import cmdline
# cmdline.execute("scrapy crawl dazhong".split())
cmdline.execute("scrapy crawl dazhong -s JOBDIR=crawls/dazhong-1".split())