# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dao import db_module

class IpPoolPipeline(object):
    table_name = 'ip_pool'
    def process_item(self, item, spider):
        sql = "insert into {} set ip_port='{}'".format(self.table_name, item.get('ip_port'))
        db_module.execute_into(sql)
        return item
