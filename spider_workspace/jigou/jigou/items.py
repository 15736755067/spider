# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JigouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    abbreviation = scrapy.Field()
    hq = scrapy.Field()
    registration_place = scrapy.Field()
    establish_date = scrapy.Field()
    capital_type = scrapy.Field()
    nature = scrapy.Field()
    stage = scrapy.Field()
    website = scrapy.Field()
    company_desc = scrapy.Field()
