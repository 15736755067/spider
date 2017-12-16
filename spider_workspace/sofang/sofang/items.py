# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SofangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    listing_price = scrapy.Field()
    city_name = scrapy.Field()
    district_name = scrapy.Field()
    built_up_area = scrapy.Field()
    greening_rate = scrapy.Field()
    floor_area = scrapy.Field()
    volume_ratio = scrapy.Field()
    total_households = scrapy.Field()
    property_fee = scrapy.Field()
    developers = scrapy.Field()
    property_company = scrapy.Field()
