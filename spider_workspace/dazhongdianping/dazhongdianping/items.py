# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DazhongdianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    execute = scrapy.Field()
    city_name = scrapy.Field()
    adname = scrapy.Field()
    business_district = scrapy.Field()
    store_id = scrapy.Field()
    brand_name = scrapy.Field()
    brand_alias = scrapy.Field()
    category_type = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    comments_num = scrapy.Field()
    total_score = scrapy.Field()
    product_score = scrapy.Field()
    environment_score = scrapy.Field()
    service_score = scrapy.Field()
    origin_comment_tags = scrapy.Field()


# class DazhongguangchangItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     city_name = scrapy.Field()
#     adname = scrapy.Field()
#     comments_count = scrapy.Field()
#     id = scrapy.Field()
#     place_name = scrapy.Field()
#     star = scrapy.Field()
#     five_star_comments_count = scrapy.Field()
#     four_star_comments_count = scrapy.Field()
#     three_star_comments_count = scrapy.Field()
#     two_star_comments_count = scrapy.Field()
#     one_star_comments_count = scrapy.Field()
#     consumption_amt = scrapy.Field()
#     type = scrapy.Field()
#     business_district = scrapy.Field()
#     address = scrapy.Field()
#     quality = scrapy.Field()
#     environment = scrapy.Field()
#     service = scrapy.Field()