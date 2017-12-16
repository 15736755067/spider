# -*- coding: utf-8 -*-
import scrapy
from ..items import FangtianxiaItem
from scrapy import Selector
from pyquery import PyQuery
class TianxiaSpider(scrapy.Spider):
    name = 'tianxia'
    allowed_domains = ['www.fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        """
        获取所有房源链接:所属省份\城市\url
        :param response:
        :return:
        """
        print response.body
        all_area = Selector(response).xpath('//tr[starts-with(@id, "sffamily_B03_29")]')
        for c_area in all_area:
            try:
                # cc_area = c_area.xpath('./td[2]/strong/text()').extract()[0]
                cc_area = "浙江"
            except:
                cc_area = None
            all_city = c_area.xpath('./td[3]/a')
            for c_content in all_city:

                c_city = c_content.xpath('./text()').extract()[0]
                c_url = c_content.xpath('./@href').extract()[0]
                dic = {"area": cc_area, "city": c_city, "url": c_url}
                item = FangtianxiaItem(dic=dic)
                yield item