# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module
class Job51SpiderreceivePipeline(object):

    def process_item(self, item, spider):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        table_name = 'worm_job51_company'
        dic = item.get('dic')
        sql = "insert into {} set city='{}',name='{}',nature='{}',size='{}',industry='{}',website='{}',address='{}'" \
              "".format(table_name, dic.get('city'), dic.get('name'), dic.get('nature'), dic.get('size'),
                        dic.get('industry'), dic.get('website'), dic.get('address'))
        db_module.execute_into(sql)
        return item
