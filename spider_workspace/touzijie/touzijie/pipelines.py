# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class TouzijiePipeline(object):
    table_name = 'worm_zdb_pedaily_ipo'
    def process_item(self, item, spider):
        sql = "insert into {} set ipo_name='{}',ipo_date='{}',invs='{}',ipo_exchange='{}',issue_price='{}'," \
              "circulation='{}',vc_pe_support='{}',stock_code='{}',name='{}'".format(self.table_name,
                                                                                     item['ipo_name'],
                                                                                     item['ipo_date'],
                                                                                     item['invs'],
                                                                                     item['ipo_exchange'],
                                                                                     item['issue_price'],
                                                                                     item['circulation'],
                                                                                     item['vc_pe_support'],
                                                                                     item['stock_code'],
                                                                                     item['name'])
        db_module.execute_into(sql)
        return item

#
# ipo_name = scrapy.Field()
# ipo_date = scrapy.Field()
# invs = scrapy.Field()
# ipo_exchange = scrapy.Field()
# issue_price = scrapy.Field()
# circulation = scrapy.Field()
# vc_pe_support = scrapy.Field()
# stock_code = scrapy.Field()
# name = scrapy.Field()
