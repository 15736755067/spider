#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..dao import db_module
def select_url(name, table_name):

    sql = u"select abbreviation from {} where abbreviation='{}'".format(table_name, name)

    ret = db_module.execute_getinfo(sql)
    return ret

def update_into(abbreviation, table_name):
    sql = u"insert into {} set abbreviation='{}', host_name='{}'".format(table_name, abbreviation)
    db_module.execute_into(sql)



# ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
# print ret