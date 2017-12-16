#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import urllib3
header = {
    "Accept": "text/html,application/json,text/javascript,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
}

# http = urllib3.PoolManager()
# ret = http.request('get', 'http://www.data5u.com/')
# print ret
ret = urllib.urlopen(url='http://www.data5u.com/', header=header)
print ret.read()