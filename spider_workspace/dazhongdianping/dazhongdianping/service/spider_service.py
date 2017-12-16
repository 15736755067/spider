#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from ..dao import db_module
def select_url(name, table_name):

    sql = u"select url_md5 from {} where url_md5='{}'".format(table_name, name)

    ret = db_module.execute_getinfo(sql)
    return ret
def select_id(store_id, table_name):
    c_time = datetime.datetime.now()
    sql = u"select create_time from {} where store_id='{}'".format(table_name, store_id)
    ret = db_module.execute_getinfo(sql)
    if ret:
        if ret[0][0].year != c_time.year or ret[0][0].month != c_time.month :
            print "update"
            return "update"
        else:
            print "ok"
            return ""
    else:
        print "into"
        return "into"

def update_into(url_md5, table_name, host_name=None):
    sql = u"insert into {} set url_md5='{}', host_name='{}'".format(table_name, url_md5, host_name)
    db_module.execute_into(sql)



# ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
# print ret