#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
def create_url():
    all_city_id = [145,]
    all_start_url = []
    url = "http://www.dianping.com/shopall/{}/0#BDBlock/"
    for city_id in all_city_id:
        start_url = url.format(city_id)
        all_start_url.append(start_url)
    return all_start_url
def create_sleep():
    ret = random.uniform(3, 5)
    time.sleep(ret)
    print ret
