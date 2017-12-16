# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from pyquery import PyQuery
from ..items import BinggouItem
from ..service import spider_service
import requests
def create_page():
    li = []
    url = 'http://zdb.pedaily.cn/ma/'
    for i in range(1, 296):
        n_url = url + 'p{}'.format(i)
        li.append(n_url)
    return li
class BingGouSpider(scrapy.Spider):
    name = 'bing_gou'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = create_page()
    header_url = 'http://zdb.pedaily.cn'
    data_table = 'worm_zdb_pedaily_ma'
    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_item)

    def parse_item(self,response):
        all_url = Selector(response=response).xpath('//*[@id="inv-list"]/li/dl/dt[5]/a/@href').extract()
        for c_url in all_url:
            n_url = self.header_url + c_url
            html = requests.get(url=n_url)
            html = html.text
            name = PyQuery(html).find('.info').find('h1').text()
            ret = spider_service.select_url(name, self.data_table)
            if not ret:
                try:
                    status = PyQuery(html).find('.info').find('li').eq(2).text().split('并购状态： ')[1]
                except Exception as e:
                    status = None
                try:
                    ma = PyQuery(html).find('.info').find('li').eq(0).text().split('并  购  方： ')[1]
                except Exception as e:
                    ma =None
                try:
                    maed = PyQuery(html).find('.info').find('li').eq(1).text().split('被并购方： ')[1]
                except Exception as e:
                    maed = None
                try:
                    equity_ratio = PyQuery(html).find('.info').find('li').eq(4).text().split('涉及股权： ')[1]
                except Exception as e:
                    equity_ratio = None
                try:
                    industry = PyQuery(html).find('.info').find('li').eq(3).text().split('所属行业： ')[1]
                except Exception as e:
                    industry = None
                try:
                    end_date = PyQuery(html).find('.info').find('li').eq(6).text().split('并购结束时间： ')[1]
                except Exception as e:
                    end_date = None
                vc_pe_support = PyQuery(html).find('.info').find('li').eq(7).text()
                event_desc = PyQuery(html).find('#desc').find('p').text()
                item = BinggouItem(name=name, status=status, ma=ma, maed=maed, equity_ratio=equity_ratio, industry=industry,
                                   end_date=end_date, vc_pe_support=vc_pe_support, event_desc=event_desc)
                yield item