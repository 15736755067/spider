# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class BinggouPipeline(object):
    table_name = 'worm_zdb_pedaily_ma'
    def process_item(self, item, spider):
        sql = "insert into {} set name='{}',status='{}',ma='{}',maed='{}',equity_ratio='{}',industry='{}'," \
              "end_date='{}',vc_pe_support='{}',event_desc='{}'".format(self.table_name,
                                                                        item['name'],
                                                                        item['status'],
                                                                        item['ma'],
                                                                        item['maed'],
                                                                        item['equity_ratio'],
                                                                        item['industry'],
                                                                        item['end_date'],
                                                                        item['vc_pe_support'],
                                                                        item['event_desc'])
        db_module.execute_into(sql)
        return item

    # name = scrapy.Field()
    # status = scrapy.Field()
    # ma = scrapy.Field()
    # maed = scrapy.Field()
    # equity_ratio = scrapy.Field()
    # industry = scrapy.Field()
    # end_date = scrapy.Field()
    # vc_pe_support = scrapy.Field()
    # event_desc = scrapy.Field()name = scrapy.Field()
