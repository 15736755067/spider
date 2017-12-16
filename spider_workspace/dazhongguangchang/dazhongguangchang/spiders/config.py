#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
def create_url():
    all_city_id = [145,]
    all_start_url = []

    for city_id in all_city_id:
        start_url = 'http://www.dianping.com/search/category/{}/20/g119/'.format(city_id)
        all_start_url.append(start_url)
    return all_start_url
def create_sleep():
    ret = random.uniform(5, 15)
    time.sleep(ret)
    print ret