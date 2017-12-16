# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongchouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_name = scrapy.Field()
    project_desc = scrapy.Field()
    project_process = scrapy.Field()
    project_tag = scrapy.Field()
    project_fundraising = scrapy.Field()
    project_support = scrapy.Field()
    fundraising_progress = scrapy.Field()
