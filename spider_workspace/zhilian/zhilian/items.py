# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    nature = scrapy.Field()
    industry = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()





    # city = scrapy.Field()
    # job_name = scrapy.Field()
    # company_name = scrapy.Field()
    # place =scrapy.Field()
    # salary = scrapy.Field()
    # job_type = scrapy.Field()
    # release_date = scrapy.Field()
    # feedback_rate = scrapy.Field()
    # numbers = scrapy.Field()
    # education = scrapy.Field()
