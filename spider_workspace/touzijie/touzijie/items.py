# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TouzijieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ipo_name = scrapy.Field()
    ipo_date = scrapy.Field()
    invs = scrapy.Field()
    ipo_exchange = scrapy.Field()
    issue_price = scrapy.Field()
    circulation = scrapy.Field()
    vc_pe_support = scrapy.Field()
    stock_code = scrapy.Field()
    name = scrapy.Field()
