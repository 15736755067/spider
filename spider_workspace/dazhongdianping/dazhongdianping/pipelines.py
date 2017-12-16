# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module


class DazhongdianpingPipeline(object):
    def process_item(self, item, spider):
        table_name = 's03_dianping_brand_info'
        sql = ''
        if item.get('execute') == 'into':
            sql = "insert into {} set city_name='{}',adname='{}',business_district='{}',store_id='{}',brand_name='{}'," \
                  "brand_alias='{}',category_type='{}',address='{}',avg_price='{}',comments_num='{}',total_score='{}'," \
                  "product_score='{}',environment_score='{}',service_score='{}',origin_comment_tags='{}'" \
                  "".format(table_name, item.get('city_name'), item.get('adname'), item.get('business_district'),
                            item.get('store_id'), item.get('brand_name'), item.get('brand_alias'),
                            item.get('category_type'), item.get('address'), item.get('avg_price'),
                            item.get('comments_num'),
                            item.get('total_score'), item.get('product_score'), item.get('environment_score'),
                            item.get('service_score'), item.get('origin_comment_tags'))
        elif item.get('execute') == 'update':
            sql = "update {} set city_name='{}',adname='{}',business_district='{}',brand_name='{}'," \
                  "brand_alias='{}',category_type='{}',address='{}',avg_price='{}',comments_num='{}',total_score='{}'," \
                  "product_score='{}',environment_score='{}',service_score='{}',origin_comment_tags='{}'" \
                  "where store_id='{}'".format(table_name, item.get('city_name'), item.get('adname'),
                                               item.get('business_district'), item.get('brand_name'),
                                               item.get('brand_alias'), item.get('category_type'), item.get('address'),
                                               item.get('avg_price'), item.get('comments_num'),
                                               item.get('total_score'), item.get('product_score'),
                                               item.get('environment_score'),item.get('service_score'),
                                               item.get('origin_comment_tags'), item.get('store_id'))
        db_module.execute_into(sql)
        return item
