# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import RongziItem
from scrapy import Selector
from ..service import spider_service
import requests
def create_page():
    li = []
    url = 'http://zdb.pedaily.cn/enterprise/'

    for i in range(1, 1622):
        n_url = url + 'p{}'.format(i)
        li.append(n_url)
    return li

class RongZiSpider(scrapy.Spider):
    name = 'rong_zi'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = create_page()
    header_url = 'http://zdb.pedaily.cn'
    table_name = 'worm_zdb_pedaily_company'
    def parse(self, response):
        all_url = Selector(response=response).xpath('//*[@id="enterprise-list"]/li/div[2]/h3/a/@href').extract()
        for c_url in all_url:
            n_url = self.header_url + c_url
            yield scrapy.Request(url=n_url, callback=self.parse_item)

    def parse_item(self, response):
        html = requests.get(url=response.url)
        html = html.text

        name = PyQuery(html).find('.info').find('h1').text().split(' ')[0]
        ret = spider_service.select_url(name, self.table_name)
        if not ret:
            abbreviation = PyQuery(html).find('.info').find('h1').find('em').text()
            try:
                hq = PyQuery(html).find('.info').find('li').eq(0).text().split('机构总部： ')[1]
            except Exception as e:
                hq = None
            try:
                registration_place = PyQuery(html).find('.info').find('li').eq(1).text().split('注册地点： ')[1]
            except Exception as e:
                registration_place = None
            try:
                establish_date = PyQuery(html).find('.info').find('li').eq(2).text().split('成立时间： ')[1]
            except Exception as e:
                establish_date = None
            try:
                industry = PyQuery(html).find('.info').find('li').eq(3).text().split('所属行业： ')[1]
            except Exception as e:
                industry = None
            try:
                website = PyQuery(html).find('.info').find('li').eq(4).text().split('官方网站： ')[1]
            except Exception as e:
                website = None

            company_desc = PyQuery(html).find('#desc').find('p').eq(1).text()
            item = RongziItem(name=name, abbreviation=abbreviation, hq=hq, registration_place=registration_place,
                              establish_date=establish_date, industry=industry, website=website, company_desc=company_desc)
            yield item