#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dao import db_module
def select_ip(ip_port, table_name):
    sql = "select ip_port from {} where ip_port='{}'".format(table_name, ip_port)
    ret = db_module.execute_getinfo(sql)
    return ret
