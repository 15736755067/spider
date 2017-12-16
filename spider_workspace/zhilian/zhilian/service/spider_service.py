#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..dao import db_module


def select_url(city=None, company_name=None, table_name=None) :

    sql = u"select name from {} where name='{}'and city='{}'".format(table_name, company_name, city)
    ret = db_module.execute_getinfo(sql)
    return ret


def update_into(url_md5, table_name, host_name=None):
    if table_name == 'worm_zhaopin_company_old':
        sql = u"insert into {} set company_name='{}',city='{}'".format(table_name, url_md5, host_name)
    else:
        sql = u"insert into {} set url_md5='{}', host_name='{}'".format(table_name, url_md5, host_name)
    db_module.execute_into(sql)



    # ret = select_url(u"fdsgdgfdgd", u"worm_url_info_housing")
    # print ret
