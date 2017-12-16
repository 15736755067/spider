#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sofangnew.dao import db_module
class Get_url:
    table_name = 'sofang_url'
    def __init__(self, province):
        self.province = province

    def __get_url(self):

        sql = "select url from {} where province='{}' and status='0'".format(self.table_name, self.province)
        ret = db_module.execute_getinfo(sql)
        return ret
    def create_list(self):
        url = []
        allowed_domains = []
        ret = self.__get_url()
        for c_url in ret:
            url.append(c_url[0])
            allowed_domains.append(c_url[0].split('//')[-1].split('/')[0])
        return [allowed_domains[0]], [url[0]]

if __name__ == '__main__':

    obj = Get_url('河南')
    print obj.create_list()