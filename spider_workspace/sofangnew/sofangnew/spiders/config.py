#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
from ..dao import db_module
# def create_url():
#     all_city_id = [145,]
#     all_start_url = []
#
#     for city_id in all_city_id:
#         start_url = 'http://www.dianping.com/search/category/{}/20/g119/'.format(city_id)
#         all_start_url.append(start_url)
#     return all_start_url
def create_sleep():
    ret = random.uniform(5, 10)
    time.sleep(ret)
    print ret

def get_info(url):
    table_name = 'sofang_url'
    sql = "select province, city from {} where url='{}'".format(table_name, url)
    ret = db_module.execute_getinfo(sql)
    sql = "update {} set status='1' where url='{}'".format(table_name, url)
    db_module.execute_into(sql)
    return ret[0][0], ret[0][1]