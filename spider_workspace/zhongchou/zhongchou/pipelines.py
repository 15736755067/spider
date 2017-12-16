# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class ZhongchouPipeline(object):
    table_name = 'worm_zhongchou'
    def process_item(self, item, spider):
        sql = "insert into {} set project_name='{}',project_desc='{}',project_process='{}',project_tag='{}'," \
              "project_fundraising='{}',project_support='{}',fundraising_progress='{}'".format(self.table_name,
                                                                                               item['project_name'],
                                                                                               item['project_desc'],
                                                                                               item['project_process'],
                                                                                               item['project_tag'],
                                                                                               item['project_fundraising'],
                                                                                               item['project_support'],
                                                                                               item['fundraising_progress'])
        db_module.execute_into(sql)
        return item
