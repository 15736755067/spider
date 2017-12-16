# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class MuziPipeline(object):
    table_name = 'worm_zdb_pedaily_pe'
    def process_item(self, item, spider):
        sql = "insert into {} set name='{}',status='{}',fund_name='{}',currency='{}',establish_date='{}',administration='{}'," \
              "capital_type='{}',amount='{}',scale='{}',event_desc='{}'".format(self.table_name,
                                                                                item['name'],
                                                                                item['status'],
                                                                                item['fund_name'],
                                                                                item['currency'],
                                                                                item['establish_date'],
                                                                                item['administration'],
                                                                                item['capital_type'],
                                                                                item['amount'],
                                                                                item['scale'],
                                                                                item['event_desc'])
        db_module.execute_into(sql)
        return item
# name = scrapy.Field()
#     fund_name = scrapy.Field()
#     status = scrapy.Field()
#     currency = scrapy.Field()
#     establish_date = scrapy.Field()
#     administration = scrapy.Field()
#     capital_type = scrapy.Field()
#     amount = scrapy.Field()
#     scale = scrapy.Field()
#     event_desc = scrapy.Field()