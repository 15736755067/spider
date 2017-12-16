#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..dao import db_module
def select_url(name, table_name):

    sql = u"select name from {} where name='{}'".format(table_name, name)

    ret = db_module.execute_getinfo(sql)
    return ret

def update_into(url_md5, table_name, host_name=None):
    sql = u"insert into {} set url_md5='{}', host_name='{}'".format(table_name, url_md5, host_name)
    db_module.execute_into(sql)



# ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
# print ret