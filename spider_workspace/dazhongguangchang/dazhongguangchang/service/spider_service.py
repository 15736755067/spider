#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
from ..dao import db_module
def select_url(name, table_name):

    sql = u"select url_md5 from {} where url_md5='{}'".format(table_name, name)

    ret = db_module.execute_getinfo(sql)
    return ret

def select_id(id, table_name):
    # c_time = time.strftime("%Y-%m$%d %H:%M:%S", time.localtime())
    # c_time = c_time.split('$')[0]
    c_time = datetime.datetime.now()
    sql = "select create_time from {} where id='{}'".format(table_name, id)
    ret = db_module.execute_getinfo(sql)
    print ret
    if ret:
        if ret[0][0].year != c_time.year or ret[0][0].month != c_time.month :
            print "update"
            return "update"
        else:
            print "ok"
            return "update"
    else:
        print "into"
        return "into"
            # sql = u"select id from {} where id='{}' and create_time".format(table_name, id)
            # ret = db_module.execute_getinfo(sql)
            # return ret
def update_into(url_md5, table_name, host_name=None):
    sql = u"insert into {} set url_md5='{}', host_name='{}'".format(table_name, url_md5, host_name)
    db_module.execute_into(sql)

# ret = time.strftime("%Y-%m$%d %H:%M:%S", time.localtime())
# print ret
# ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
# print ret