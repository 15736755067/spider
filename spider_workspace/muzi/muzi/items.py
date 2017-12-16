# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    fund_name = scrapy.Field()
    status = scrapy.Field()
    currency = scrapy.Field()
    establish_date = scrapy.Field()
    administration = scrapy.Field()
    capital_type = scrapy.Field()
    amount = scrapy.Field()
    scale = scrapy.Field()
    event_desc = scrapy.Field()
