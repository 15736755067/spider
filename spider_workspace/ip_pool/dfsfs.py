#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
ret = requests.get('http://www.baidu.com')
print ret.text
