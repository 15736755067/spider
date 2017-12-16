# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .dao import db_module

class ZhilianPipeline(object):
    # table_name = u'worm_zhaopin'
    table_name = 'worm_zhaopin_company'
    def process_item(self, item, spider):
        sql = "insert into {} set city='{}',name='{}',size='{}',nature='{}',industry='{}',website='{}',address='{}'" \
              "".format(self.table_name, item.get('city'), item.get('name'), item.get('size'), item.get('nature'), item.get('industry'),
                        item.get('website'), item.get('address'))
        # sql = "insert into {} set city='{}',job_name='{}',company_name='{}',place='{}',salary='{}',job_type='{}'," \
        #       "release_date='{}',feedback_rate='{}',numbers='{}',education='{}'".format(self.table_name,
        #                                                                                 item['city'],
        #                                                                                 item['job_name'],
        #                                                                                 item['company_name'],
        #                                                                                 item['place'],
        #                                                                                 item['salary'],
        #                                                                                 item['job_type'],
        #                                                                                 item['release_date'],
        #                                                                                 item['feedback_rate'],
        #                                                                                 item['numbers'],
        #                                                                                 item['education'])
        db_module.execute_into(sql)
        return item
# city = scrapy.Field()
#     name = scrapy.Field()
#     size = scrapy.Field()
#     nature = scrapy.Field()
#     industry = scrapy.Field()
#     website = scrapy.Field()
#     address = scrapy.Field()