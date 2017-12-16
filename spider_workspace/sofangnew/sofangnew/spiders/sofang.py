# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import Selector
from ..items import SofangnewItem
from ..get_url.get_url import Get_url
from pyquery import PyQuery
from config import create_sleep, get_info
import time
obj = Get_url('河北')

class SofangSpider(scrapy.Spider):

    name = 'sofang'
    allowed_domains, start_urls = obj.create_list()
    def __init__(self):
        dispatcher.connect(self.spider_stoped, signals.engine_stopped)
    def spider_stoped(self):
        f = open('ok.txt', 'w')
    # def parse(self, response):
    #     all_area = Selector(response).xpath('/html/body/div[2]/div[3]/div[2]/ul[1]/li[1]')
    #     print len(all_area)
    #     for c_area in all_area:
    #
    #         province = c_area.xpath('./label/i/text()').extract()[0]
    #
    #         all_city = c_area.xpath('./p/a')
    #         print len(all_city)
    #         for c_city in all_city:
    #             city_name = c_city.xpath('./text()').extract()[0]
    #             url = c_city.xpath('./@href').extract()[0] + '/saleesb/area'
    #             dic = {"province": province, "city_name": city_name}
    #             create_sleep()
    #             yield scrapy.Request(url=url, meta=dic, callback=self.parse_area)
                # dic = {"province": province, "city": city, "url": url}
                # item = SofangnewItem(dic=dic)
                # yield item
    def parse(self, response):
        """
        获取区域url
        :param response:
        :return:
        """
        province, city_name = get_info(response.url)
        dic = {"province": province, "city_name": city_name}
        all_area = Selector(response).xpath('/html/body/div[4]/div[3]/div/dl[1]/dd[1]/a')
        for i in range(1, len(all_area)):
            c_area = all_area[i].xpath('./text()').extract()[0]
            dic['area'] = c_area
            c_url = response.url + '/' + all_area[i].xpath('./@href').extract()[0].split('/')[-1]
            create_sleep()
            yield scrapy.Request(url=c_url, meta=dic, callback=self.parse_all_page)

    def parse_all_page(self, response):
        """
        获取最大页url,生成所有页url
        :param response:
        :return:
        """
        dic = response.meta
        try:
            max_page_li = Selector(response).xpath('/html/body/div[4]/div[4]/div[1]/div[3]/ul/li')[-3]
        except:
            max_page_li = None
        if max_page_li != None:
            try:
                max_page = max_page_li.xpath('./a/text()').extract()[0]
            except:
                max_page = None
            if max_page:
                max_page_url = max_page_li.xpath('./a/@href').extract()[0]
                head_url = response.url
                for i in range(1, int(max_page) + 1):
                    n_page_url = head_url + "-bl{}".format(i)
                    create_sleep()
                    yield scrapy.Request(url=n_page_url, meta=dic, callback=self.parse_page)
            else:
                create_sleep()
                yield scrapy.Request(url=response.url, meta=dic, callback=self.parse_page)
        else:
            create_sleep()
            yield scrapy.Request(url=response.url, meta=dic, callback=self.parse_page)

    def parse_page(self, response):
        """
        获取当前页小区url
        :param response:
        :return:
        """
        dic = response.meta
        # city_name = Selector(response).xpath('//*[@id="city"]/a/span/text()').extract()[0]
        all_url = Selector(response).xpath('/html/body/div[4]/div[4]/div[1]/div[2]/dl/dd[1]/p/a/@href').extract()
        heade_url = response.url.split('//')[-1].split('/')[0]
        for c_url in all_url:
            n_url = "http://" + heade_url + c_url
            create_sleep()
            yield scrapy.Request(url=n_url, meta=dic, callback=self.parse_name)

    def parse_name(self, response):
        """
        获取所需的字段
        :param response:
        :return:
        """
        city_name = response.meta.get('city_name')
        html = response.body
        ret = PyQuery(html).find('.real_detail')
        ret = PyQuery(ret).find('span')
        try:
            name = PyQuery(html).find('.conTop_title').children('h2').text()
        except:
            name = None
        try:
            address = PyQuery(ret[-1]).text()
        except:
            address = None
        try:
            listing_price = PyQuery(html).find('.price').text().split(' ')[0]
        except:
            listing_price = None
        try:
            district_name = PyQuery(ret[8]).text().strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '')
        except:
            district_name = None
        try:
            built_up_area = PyQuery(ret[3]).text().split(' ')[0]
        except:
            built_up_area = None
        try:
            floor_area = PyQuery(ret[4]).text().split(' ')[0]
        except:
            floor_area = None
        try:
            total_households = PyQuery(ret[5]).text().split(' ')[0]
        except:
            total_households = None
        try:
            greening_rate = PyQuery(ret[6]).text().split(' ')[0]
        except:
            greening_rate = None
        try:
            volume_ratio = PyQuery(ret[7]).text()
        except:
            volume_ratio = None
        try:
            property_fee = PyQuery(ret[11]).text().split(' ')[0]
        except:
            property_fee = None
        try:
            developers = PyQuery(ret[12]).text()
        except:
            developers = None
        try:
            property_company = PyQuery(ret[13]).text()
        except:
            property_company = None
        dic = {"name": name, "city_name": city_name, "listing_price": listing_price, "address": address,
               "district_name": district_name, "built_up_area": built_up_area, "greening_rate": greening_rate,
               "floor_area": floor_area, "volume_ratio": volume_ratio, "total_households": total_households,
               "property_fee": property_fee, "developers": developers, "property_company": property_company
               }
        item = SofangnewItem(dic=dic)
        yield item