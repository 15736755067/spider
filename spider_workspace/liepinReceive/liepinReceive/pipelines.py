# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .dao import db_module


class LiepinreceivePipeline(object):
    def process_item(self, item, spider):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        table_name = 'worm_liepin_company'
        ret = item.get('dic')
        sql = "insert into {} set city='{}', name='{}',nature='{}',size='{}',industry='{}',address='{}'" \
              "".format(table_name, ret.get('city'), ret.get('name'), ret.get('nature'),
                                               ret.get('size'), ret.get('industry'),
                                               ret.get('address'))
        db_module.execute_into(sql)
        return item
