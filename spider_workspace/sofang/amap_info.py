#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from sofang.dao import db_module
from sofang.service import amapapi
city = '上海市'
sql = 'SELECT DISTINCT(name) from worm_housing_lianjia'

xiaoqu_list = db_module.execute_getinfo(sql)
obj = amapapi.AMAPApi()

for c_name in xiaoqu_list:
    cc_name = c_name[0]
    time.sleep(1)
    ret = obj.get_place_poi(city=city, keywords=cc_name, types='120300')
    if ret[1]:

        amap_id = ret[1][0].get('place_id')
        amap_location = ret[1][0].get('place_location')
        print amap_id, amap_location
        sql = "update worm_housing_lianjia set amap_id='{}',amap_location='{}' where name ='{}'".format(amap_id,
                                                                                                      amap_location,
                                                                                                      cc_name)
        db_module.execute_into(sql)