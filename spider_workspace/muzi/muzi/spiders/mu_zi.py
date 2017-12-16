# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from pyquery import PyQuery
from ..items import MuziItem
from ..service import spider_service
import requests
def create_page():
    li = []
    url = 'http://zdb.pedaily.cn/pe/'
    for i in range(1, 502):
        n_url = url + 'p{}'.format(i)
        li.append(n_url)
    return li
class MuZiSpider(scrapy.Spider):
    name = 'mu_zi'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = create_page()
    header_url = 'http://zdb.pedaily.cn'
    data_table = 'worm_zdb_pedaily_pe'
    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_item)
    def parse_item(self, response):
        all_url = Selector(response=response).xpath('//*[@id="pe-list"]/li/dl/dt[4]/a/@href').extract()
        for c_url in all_url:
            n_url = self.header_url + c_url
            html = requests.get(url=n_url)
            html = html.text
            name = PyQuery(html).find('.info').find('h1').text()
            ret = spider_service.select_url(name, self.data_table)
            if not ret:
                try:
                    fund_name = PyQuery(html).find('.info').find('li').eq(0).text().split('基金名称： ')[1]
                except Exception as e:
                    fund_name = None
                try:
                    status = PyQuery(html).find('.info').find('li').eq(3).text().split('募集状态： ')[1]
                except Exception as e:
                    status = None
                try:
                    currency = PyQuery(html).find('.info').find('li').eq(1).text().split('币 种： ')[1]
                except Exception as e:
                    currency = None
                try:
                    establish_date = PyQuery(html).find('.info').find('li').eq(2).text().split('成立时间： ')[1]
                except Exception as e:
                    establish_date = None
                try:
                    administration = PyQuery(html).find('.info').find('li').eq(4).text().split('管理机构： ')[1]
                except Exception as e:
                    administration = None
                try:
                    capital_type = PyQuery(html).find('.info').find('li').eq(6).text().split('资本类型： ')[1]
                except Exception as e:
                    capital_type = None
                try:
                    amount = PyQuery(html).find('.info').find('li').eq(7).text().split('募集金额： ')[1]
                except Exception as e:
                    amount = None
                try:
                    scale = PyQuery(html).find('.info').find('li').eq(5).text().split('目标规模： ')[1]
                except Exception as e:
                    scale = None
                try:
                    event_desc = PyQuery(html).find('#desc').find('p').text()
                except Exception as e:
                    event_desc = None
                item = MuziItem(name=name, fund_name=fund_name, status=status , currency=currency,
                                   establish_date=establish_date, administration=administration, capital_type=capital_type,
                                   amount=amount, scale=scale, event_desc=event_desc)
                yield item
