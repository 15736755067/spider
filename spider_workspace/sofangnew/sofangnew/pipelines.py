# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class SofangnewPipeline(object):
    def process_item(self, item, spider):
        table_name = "worm_housing_sofang"
        ret = item.get('dic')
        # sql = "insert into {} set province='{}',city='{}',url='{}'".format(table_name,
        #                                                                    ret.get('province'),
        #                                                                    ret.get('city'),
        #                                                                    ret.get('url'))
        sql = u"insert into {} set name='{}',address='{}',listing_price='{}',city_name='{}',district_name='{}'," \
              u"built_up_area='{}',greening_rate='{}',floor_area='{}',volume_ratio='{}',total_households='{}'," \
              u"property_fee='{}',developers='{}',property_company='{}'".format(table_name, ret['name'],
                                                                                ret['address'],
                                                                                ret['listing_price'],
                                                                                ret['city_name'],
                                                                                ret['district_name'],
                                                                                ret['built_up_area'],
                                                                                ret['greening_rate'],
                                                                                ret['floor_area'],
                                                                                ret['volume_ratio'],
                                                                                ret['total_households'],
                                                                                ret['property_fee'],
                                                                                ret['developers'],
                                                                                ret['property_company'])
        db_module.execute_into(sql)
        return item
