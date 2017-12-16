#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
from header import create_header
import requests
# li = (datetime.Datetime(2017, 9, 17, 11, 55, 51))
html = requests.get(url='http://www.xicidaili.com/nn/1')
print html.text