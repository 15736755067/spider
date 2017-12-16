#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy import Selector
from pyquery import PyQuery
from ..items import DazhongdianpingItem
from ..service import spider_service
from ..header.create_header import *
from config import create_url, create_sleep
import time

import re


# print "请输入城市id"
# key = int(raw_input())



class DazhongSpider(scrapy.Spider):
    name = 'dazhong'
    allowed_domains = ['dianping.com']
    start_urls = create_url()
    header_url = 'http://www.dianping.com'
    # city_name = '淄博'
    md5_table = 'worm_url_info_dazhong'
    data_table = 's03_dianping_brand_info'

    def parse(self, response):
        """
        解析获取商圈url
        :param response:
        :return:
        """

        try:
            all_area = Selector(response).xpath('//*[@id="top"]/div[6]/div/div[2]/dl[1]')
        except Exception as e:
            all_area = []
        for c_area in all_area:
            adname = c_area.xpath('./dt/a/text()').extract()[0]
            all_url = c_area.xpath('./dd/ul/li/a/@href').extract()
            all_text = c_area.xpath('./dd/ul/li/a/text()').extract()
            for c_url in range(len(all_url)):
                n_url = self.header_url + all_url[c_url]
                create_sleep()
                yield scrapy.Request(url=n_url, meta={'item': adname, 'business_district': all_text[c_url]},
                                     callback=self.parse_business_district, headers=header)

    def parse_business_district(self, response):
        """
        解析商圈url,获取所属业态url
        :param response:
        :return:
        """
        city_name = Selector(response).xpath('//*[@id="logo-input"]/div/a[2]/span/text()').extract()[0]
        business_district = response.meta.get('business_district')
        adname = response.meta.get('item')
        all_url = Selector(response=response).xpath('/html/body/div[2]/div[2]/div[1]/div/div/div/a/@href').extract()
        all_text = Selector(response=response).xpath(
            '/html/body/div[2]/div[2]/div[1]/div/div/div/a/span/text()').extract()
        for c_url in range(len(all_url)):
            create_sleep()
            dic = {'item': adname,
                   'business_district': business_district,
                   'category_type': all_text[c_url],
                   'city_name': city_name
                   }
            yield scrapy.Request(url=all_url[c_url], meta=dic, callback=self.parse_category_type, headers=header1)

    def parse_category_type(self, response):
        """
        解析业态url,获取页码url
        :param response:
        :return:
        """
        city_name = response.meta.get('city_name')
        category_type = response.meta.get('category_type')
        business_district = response.meta.get('business_district')
        adname = response.meta.get('item')
        dic = {'item': adname,
               'business_district': business_district,
               'category_type': category_type,
               'city_name': city_name
               }
        try:
            all_page = PyQuery(response.body).find('.page').find('a').eq(-2).attr('href')
        except:
            all_page = None
        if all_page:
            num = all_page.split('/')[-1].split('p')[-1]
            try:
                c_num, aid = num.split('?')
            except:
                c_num = num
                aid = ""
            head, head1, mid, end = all_page.split('p')

            for c_page in range(1, int(c_num) + 1):
                if aid == '':
                    n_page = head + 'p' + head1 + 'p' + mid + 'p{}'.format(c_page)
                else:
                    n_page = head + 'p' + head1 + 'p' + mid + 'p{}'.format(c_page) + '?' + aid
                md5_url = self.md5(n_page)
                ret = spider_service.select_url(md5_url, self.md5_table)
                if not ret:
                    create_sleep()
                    spider_service.update_into(md5_url, self.md5_table)
                    yield scrapy.Request(url=n_page, meta=dic, callback=self.parse_page, headers=header2)


        else:
            time.sleep(3)
            md5_url = self.md5(response.url)
            spider_service.update_into(md5_url, self.md5_table)
            yield scrapy.Request(url=response.url, meta=dic, callback=self.parse_page, headers=header3)

    def parse_page(self, response):
        """
        解析页面url, 获取店铺url
        :param response:
        :return:
        """
        city_name = response.meta.get('city_name')
        category_type = response.meta.get('category_type')
        business_district = response.meta.get('business_district')
        adname = response.meta.get('item')
        all_url = Selector(response=response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/@href').extract()
        # header["User-Agent"] = get_user_agent()
        dic = {'item': adname,
               'business_district': business_district,
               'category_type': category_type,
               'city_name': city_name
               }

        for c_url in all_url:

            store_id = c_url.split('/')[-1]
            ret = spider_service.select_id(store_id, self.data_table)
            dic['execute'] = ret
            if ret:
                create_sleep()
                yield scrapy.Request(url=c_url, meta=dic, callback=self.parse_brand, headers=create_header())
            else:
                pass

    def parse_brand(self, response):
        """
        解析店铺url,
        :param response:
        :return:
        """
        execute = response.meta.get('key')
        category_type = response.meta.get('category_type')
        business_district = response.meta.get('business_district')
        city_name = response.meta.get('city_name')
        try:
            store_id = response.url.split('/')[-1]
        except:
            store_id = None
        try:
            adname = response.meta.get('item')
        except:
            adname = None
        try:
            key = Selector(response=response).xpath('//*[@id="basic-info"]/div[4]/p[1]/span[1]/text()').extract()[0]
        except:
            key = None
        if key == '别       名：':
            try:
                brand_alias = \
                    Selector(response=response).xpath('//*[@id="basic-info"]/div[4]/p[1]/span[2]/text()').extract()[
                        0].strip()
            except:
                brand_alias = None
        else:
            brand_alias = None
        try:
            product_score = \
                Selector(response=response).xpath('//*[@id="comment_score"]/span[1]/text()').extract()[0].split('：')[-1]
        except:
            product_score = 0
        try:
            environment_score = \
                Selector(response=response).xpath('//*[@id="comment_score"]/span[2]/text()').extract()[0].split(
                    '：')[-1]
        except:
            environment_score = 0
        try:
            service_score = \
                Selector(response=response).xpath('//*[@id="comment_score"]/span[3]/text()').extract()[0].split(
                    '：')[-1]
        except:
            service_score = 0
        try:
            origin_comment_tags_list = Selector(response=response).xpath(
                '//*[@id="summaryfilter-wrapper"]/div[1]/div[2]/span/text').extract()
        except:
            origin_comment_tags_list = []
        origin_comment_tags = ''
        for i in origin_comment_tags_list:
            origin_comment_tags = origin_comment_tags + " " + i

        if category_type == '学习培训':

            try:
                brand_name = \
                    Selector(response=response).xpath(
                        '//*[@id="top"]/div[5]/div/div[1]/div[1]/div[1]/h1/text()').extract()[0].strip()
            except:
                brand_name = None

            try:
                address = Selector(response=response).xpath(
                    '//*[@id="top"]/div[5]/div/div[1]/div[1]/div[2]/div[2]/div[2]/text()').extract()[0].strip()
            except:
                address = None
            try:
                avg_price = \
                    Selector(response=response).xpath('//*[@id="avgPriceTitle"]/text()').extract()[0].split('：')[-1]
                if avg_price == '-':
                    avg_price = None
            except:
                avg_price = None
            try:
                comments_num = \
                    Selector(response=response).xpath(
                        '//*[@id="top"]/div[5]/div/div[1]/div[1]/div[2]/div[2]/div[1]/a/span/text()').extract()[
                        0].split('条评论')[0]
            except:
                comments_num = None
            try:
                total_score = \
                    Selector(response=response).xpath(
                        '//*[@id="top"]/div[5]/div/div[1]/div[1]/div[2]/div[2]/div[1]/span[1]/@class').extract()[
                        0].split('str')[-1]

                if total_score == '10':
                    total_score = "一星商户"
                elif total_score == '20':
                    total_score = "二星商户"
                elif total_score == '30':
                    total_score = "三星商户"
                elif total_score == '35':
                    total_score = "准四星商户"
                elif total_score == '40':
                    total_score = "四星商户"
                elif total_score == '45':
                    total_score = "准五星商户"
                elif total_score == '50':
                    total_score = "五星商户"
                else:
                    total_score = "该商户暂无星级"
            except:
                total_score = None
        elif category_type == '家装':

            try:
                brand_name = Selector(response=response).xpath(
                    '//*[@id="J_boxDetail"]/div/div[1]/h1/text()').extract()[0].strip()
            except:
                brand_name = None

            try:
                address = Selector(response=response).xpath(
                    '//*[@id="J_boxDetail"]/div/p/text()').extract()[0].strip()
            except:
                address = None
            try:
                avg_price = \
                    Selector(response=response).xpath('//*[@id="avgPriceTitle"]/text()').extract()[0].split('：')[-1]
                if avg_price == '-':
                    avg_price = None
            except:
                avg_price = None
            try:
                comments_num = Selector(response=response).xpath(
                    '//*[@id="J_boxDetail"]/div/div[2]/a/text()').extract()[0].split('条评论')[0]
            except:
                comments_num = None
            try:
                total_score = \
                    Selector(response=response).xpath('//*[@id="J_boxDetail"]/div/div[2]/span/@title').extract()[0]
            except:
                total_score = None

        else:

            try:
                brand_name = Selector(response=response).xpath('//*[@id="basic-info"]/h1/text()').extract()[
                    0].strip()
            except:
                brand_name = None

            try:
                address = \
                    Selector(response=response).xpath('//*[@id="basic-info"]/div[2]/span[2]/text()').extract()[
                        0].strip()
            except:
                address = None
            try:
                avg_price = \
                    Selector(response=response).xpath('//*[@id="avgPriceTitle"]/text()').extract()[0].split('：')[-1]
                if avg_price == '-':
                    avg_price = None
            except:
                avg_price = None
            try:
                comments_num = \
                    Selector(response=response).xpath('//*[@id="reviewCount"]/text()').extract()[0].split('条评论')[0]
            except:
                comments_num = None
            try:
                total_score = \
                    Selector(response=response).xpath('//*[@id="basic-info"]/div[1]/span[1]/@title').extract()[0]
            except:
                total_score = None
        item = DazhongdianpingItem(city_name=city_name, adname=adname, business_district=business_district,
                                   store_id=store_id, brand_name=brand_name, brand_alias=brand_alias,
                                   category_type=category_type, address=address, avg_price=avg_price,
                                   comments_num=comments_num, total_score=total_score, product_score=product_score,
                                   environment_score=environment_score, service_score=service_score,
                                   origin_comment_tags=origin_comment_tags, execute=execute)
        yield item

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(url)
        return obj.hexdigest()
