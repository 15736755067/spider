#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import time
from sofang.dao import db_module

sql = 'SELECT DISTINCT(amap_id) from worm_housing_sofang'
id_list = db_module.execute_getinfo(sql)
print id_list
# proxies = {"http": "101.81.108.117:9000", }
# for c_id in id_list:
#     # print c_id[0]
#     if c_id[0]:
#         url = 'http://www.gaode.com/detail/get/detail?id={}'.format(c_id[0])
#
#         ret = requests.get(url=url, proxies=proxies)
#         print ret.text
#         dic = json.loads(ret)
#         # print ret
#         time.sleep(10)
#         c_dic = dic.get('data').get('spec').get('mining_shape')
#         amap_id = c_id[0]
#         amap_shape = c_dic.get('shape')
#         area = c_dic.get('area')
#         center_location = c_dic.get('center')
#         sql = "insert into worm_housing_shape_sofang set amap_id='{}'," \
#               "amap_shape='{}',area='{}',center_location='{}'".format(amap_id, amap_shape, area, center_location)
#         db_module.execute_into(sql)
