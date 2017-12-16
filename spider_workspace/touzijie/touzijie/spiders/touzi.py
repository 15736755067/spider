# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from pyquery import PyQuery
from ..items import TouzijieItem
from ..service import spider_service
header = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'Hm_lvt_25919c38fb62b67cfb40d17ce3348508=1506068407; Hm_lpvt_25919c38fb62b67cfb40d17ce3348508=1506069232; __utma=23980325.2136428885.1506068407.1506068407.1506068407.1; __utmc=23980325; __utmz=23980325.1506068407.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); jiathis_rdc=%7B%22http%3A//zdb.pedaily.cn/ipo/show36330/%22%3A%220%7C1506069232716%22%7D',
'Host':'zdb.pedaily.cn',
'Referer':'http://zdb.pedaily.cn/ipo/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}
import requests
def create_page():
    li = []
    url = 'http://zdb.pedaily.cn/ipo/'
    for i in range(1, 893):
        n_url = url + 'p{}'.format(i)
        li.append(n_url)
    return li
class TouziSpider(scrapy.Spider):
    name = 'touzi'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = create_page()
    header_url = 'http://zdb.pedaily.cn'
    data_table = 'worm_zdb_pedaily_ipo'
    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_item)
    def parse_item(self, response):
        all_url = Selector(response=response).xpath('//*[@id="ipo-list"]/li/dl/dt[5]/a/@href').extract()
        for c_url in all_url:
            n_url = self.header_url + c_url
            # response = HtmlResponse(url='http://example.com', body=body)
            html = requests.get(url=n_url)
            html = html.text
            ipo_name = PyQuery(html).find('.info').find('h1').text()
            ret = spider_service.select_url(ipo_name, self.data_table)
            if not ret:
                try:
                    ipo_date = PyQuery(html).find('.info').find('li').eq(3).text().split('上市时间： ')[1]
                except Exception as e:
                    ipo_date = None
                try:
                    invs = PyQuery(html).find('.info').find('li').eq(2).text().split('投  资  方： ')[1]
                except Exception as e:
                    invs = None
                try:
                    ipo_exchange = PyQuery(html).find('.info').find('li').eq(5).find('a').text()
                except Exception as e:
                    ipo_exchange = None
                try:
                    issue_price = PyQuery(html).find('.info').find('li').eq(4).text().split('发  行  价： ')[1]
                except Exception as e:
                    issue_price = None
                try:
                    circulation = PyQuery(html).find('.info').find('li').eq(6).text().split('发  行  量： ')[1]
                except Exception as e:
                    circulation = None
                try:
                    vc_pe_support = PyQuery(html).find('.info').find('li').eq(8).text()
                except Exception as e:
                    vc_pe_support = None
                try:
                    stock_code = PyQuery(html).find('.info').find('li').eq(7).text().split('股票代码： ')[1]
                except Exception as e:
                    stock_code = None
                try:
                    name = PyQuery(html).find('.info').find('li').eq(0).text().split('公司名称： ')[1]
                except Exception as e:
                    name = None
                item = TouzijieItem(ipo_name=ipo_name, ipo_date=ipo_date, invs=invs, ipo_exchange=ipo_exchange,
                                    issue_price=issue_price, circulation=circulation, vc_pe_support=vc_pe_support,
                                    stock_code=stock_code, name=name)
                yield item
