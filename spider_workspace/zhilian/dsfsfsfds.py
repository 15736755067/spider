#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
url = 'http://jobs.zhaopin.com/537643683250010.htm?ssidkey=y&ss=201&ff=03&sg=5bf9333c0c424479894d9431dde4088d&so=2'
html = requests.get(url=url)
print html.text