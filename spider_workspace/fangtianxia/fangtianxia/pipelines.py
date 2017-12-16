# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module


class FangtianxiaPipeline(object):
    def process_item(self, item, spider):
        table_name = 'fangtianxia_url'
        ret = item.get('dic')
        # sql = "insert into {} set province='{}',city='{}',url='{}'".format(table_name,
        #                                                                    ret.get('area'),
        #                                                                    ret.get('city'),
        #                                                                    ret.get('url'))
        sql = "update {} set province='{}',city='{}',url='{}' where city='{}'".format(table_name,
                                                                                      ret.get('area'),
                                                                                      ret.get('city'),
                                                                                      ret.get('url'),
                                                                                      ret.get('city'))
        db_module.execute_into(sql)
        return item
