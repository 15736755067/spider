# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .dao import db_module

class SofangPipeline(object):
    table_name = 'worm_housing_sofang'
    def process_item(self, item, spider):



        sql = u"insert into {} set name='{}',address='{}',listing_price='{}',city_name='{}',district_name='{}'," \
            u"built_up_area='{}',greening_rate='{}',floor_area='{}',volume_ratio='{}',total_households='{}'," \
            u"property_fee='{}',developers='{}',property_company='{}'".format(self.table_name, item['name'],
                                                                                    item['address'],
                                                                                    item['listing_price'],
                                                                                    item['city_name'],
                                                                                    item['district_name'],
                                                                                    item['built_up_area'],
                                                                                    item['greening_rate'],
                                                                                    item['floor_area'],
                                                                                    item['volume_ratio'],
                                                                                    item['total_households'],
                                                                                    item['property_fee'],
                                                                                    item['developers'],
                                                                                    item['property_company'])
        db_module.execute_into(sql)

        return item
