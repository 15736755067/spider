# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .dao import db_module

class DazhongguangchangPipeline(object):
    def process_item(self, item, spider):
        table_name = 's04_dianping_plaze_info'
        ret = item.get('dic')
        print ret
        if ret.get('execute') == "into":
            sql = "insert into {} set city_name='{}',adname='{}',comments_count='{}',id='{}',place_name='{}',star='{}'," \
                  "five_star_comments_count='{}',four_star_comments_count='{}',three_star_comments_count='{}'," \
                  "two_star_comments_count='{}',one_star_comments_count='{}',consumption_amt='{}',type='{}'," \
                  "business_district='{}',address='{}',quality='{}',environment='{}',service='{}'" \
                  "".format(table_name, ret.get('city_name'), ret.get('adname'), ret.get('comments_count'),
                            ret.get('id'), ret.get('place_name'), ret.get('star'),
                            ret.get('five_star_comments_count'),
                            ret.get('four_star_comments_count'), ret.get('three_star_comments_count'),
                            ret.get('two_star_comments_count'), ret.get('one_star_comments_count'),
                            ret.get('consumption_amt'), ret.get('type'), ret.get('business_district'),
                            ret.get('address'), ret.get('quality'), ret.get('environment'), ret.get('service'))
        elif ret.get('execute') == "update":
            sql = "update {} set city_name='{}',adname='{}',comments_count='{}',place_name='{}',star='{}'," \
                  "five_star_comments_count='{}',four_star_comments_count='{}',three_star_comments_count='{}'," \
                  "two_star_comments_count='{}',one_star_comments_count='{}',consumption_amt='{}',type='{}'," \
                  "business_district='{}',address='{}',quality='{}',environment='{}',service='{}' where id='{}'" \
                  "".format(table_name, ret.get('city_name'), ret.get('adname'), ret.get('comments_count'),
                            ret.get('place_name'), ret.get('star'),ret.get('five_star_comments_count'),
                            ret.get('four_star_comments_count'), ret.get('three_star_comments_count'),
                            ret.get('two_star_comments_count'), ret.get('one_star_comments_count'),
                            ret.get('consumption_amt'), ret.get('type'), ret.get('business_district'),
                            ret.get('address'), ret.get('quality'), ret.get('environment'), ret.get('service'),
                            ret.get('id'))
        db_module.execute_into(sql)
        return item
