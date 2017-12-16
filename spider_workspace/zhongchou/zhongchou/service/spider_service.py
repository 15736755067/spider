#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..dao import db_module
def select_url(url_md5, table_name):
    sql =u''
    if table_name == u'worm_url_info_housing':
        sql = u"select url_md5 from {} where url_md5='{}'".format(table_name, url_md5)
    elif table_name == u'worm_housing_lianjia':
        sql = u"select name from {} where name='{}'".format(table_name, url_md5)
    elif table_name == u'worm_url_info_housing_sou':
        sql = u"select url_md5 from {} where url_md5='{}'".format(table_name, url_md5)
    elif table_name == u'worm_url_info_zhong_chou':
        sql = u"select url_md5 from {} where url_md5='{}'".format(table_name, url_md5)
    ret = db_module.execute_getinfo(sql)
    return ret

def update_into(url_md5, table_name, host_name=None):
    sql = u"insert into {} set url_md5='{}', host_name='{}'".format(table_name, url_md5, host_name)
    db_module.execute_into(sql)



# ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
# print ret