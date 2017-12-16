# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BinggouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
    ma = scrapy.Field()
    maed = scrapy.Field()
    equity_ratio = scrapy.Field()
    industry = scrapy.Field()
    end_date = scrapy.Field()
    vc_pe_support = scrapy.Field()
    event_desc = scrapy.Field()
