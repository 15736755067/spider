# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class RongziPipeline(object):
    table_name = 'worm_zdb_pedaily_company'
    def process_item(self, item, spider):
        sql = "insert into {} set name='{}',abbreviation='{}',hq='{}',registration_place='{}',establish_date='{}'," \
              "industry='{}',website='{}',company_desc='{}'".format(self.table_name, item['name'], item['abbreviation'],
                                                                    item['hq'], item['registration_place'],
                                                                    item['establish_date'], item['industry'],
                                                                    item['website'],item['company_desc'])
        db_module.execute_into(sql)
        return item
# name = scrapy.Field()
#     abbreviation = scrapy.Field()
#     hq = scrapy.Field()
#     registration_place = scrapy.Field()
#     establish_date = scrapy.Field()
#     industry = scrapy.Field()
#     website = scrapy.Field()
#     company_desc = scrapy.Field()
