# -*- coding: utf-8 -*-
import scrapy
import requests
from ..items import JigouItem
from ..service import spider_service
from scrapy import Selector
from pyquery import PyQuery
def create_page():
    li = []
    url = 'http://zdb.pedaily.cn/company/all'
    for i in range(1, 775):
        n_url = url + '-p{}'.format(i)
        li.append(n_url)
    return li


class JiGouSpider(scrapy.Spider):
    name = 'ji_gou'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = create_page()
    header_url = u'http://zdb.pedaily.cn'
    table_name = u'worm_zdb_pedaily_iinew'
    def parse(self, response):
        all_url = Selector(response=response).xpath('//*[@id="company-list"]/li/div[2]/h3/a/@href').extract()
        for c_url in all_url:
            n_url = self.header_url + c_url
            yield scrapy.Request(url=n_url, callback=self.parse_item)
    def parse_item(self, response):
        html = requests.get(response.url)
        html = html.text
        try:
            abbreviation = PyQuery(html).find('.info').find('h1').find('em').text()
        except Exception as e:
            abbreviation = None
        ret = spider_service.select_url(abbreviation, self.table_name)
        if not ret:
            try:
                name = PyQuery(html).find('.info').find('h1').text().split(' {}'.format(abbreviation))[0]

            except Exception as e:

                name = None

            try:
                hq = PyQuery(html).find('.info').find('li').eq(4).text().split('机构总部： ')[1]
            except Exception as e:
                hq = None
            try:
                registration_place = PyQuery(html).find('.info').find('li').eq(2).text().split('注册地点： ')[1]
            except Exception as e:
                registration_place = None
            try:
                establish_date = PyQuery(html).find('.info').find('li').eq(3).text().split('成立时间： ')[1]
            except Exception as e:
                establish_date = None
            try:
                capital_type = PyQuery(html).find('.info').find('li').eq(0).text().split('资本类型： ')[1]
            except Exception as e:
                capital_type = None
            try:
                nature = PyQuery(html).find('.info').find('li').eq(1).text().split('机构性质： ')[1]
            except Exception as e:
                nature = None
            try:
                stage = PyQuery(html).find('.info').find('li').eq(6).text().split('投资阶段： ')[1]
            except Exception as e:
                stage = None
            try:
                website = PyQuery(html).find('.info').find('li').eq(5).find('a').text()
            except Exception as e:
                website = None
            company_desc_list = [PyQuery(i).text() for i in PyQuery(html).find('#cke_pastebin').find('#cke_pastebin')]
            company_desc = ''
            if company_desc_list:
                for i in company_desc_list:
                    company_desc = company_desc + i
            else:
                company_desc = company_desc + PyQuery(html).find('#cke_pastebin').text()
                if not company_desc:
                    company_desc = PyQuery(html).find('#desc').find('p').text()
                    if not company_desc:
                        company_desc = PyQuery(html).find('#desc').find('div').text()
            item = JigouItem(name=name, abbreviation=abbreviation, hq=hq, registration_place=registration_place,
                             establish_date=establish_date, capital_type=capital_type, nature=nature, stage=stage,
                             website=website, company_desc=company_desc)
            yield item
        # else:
        #     spider_service.update_into(abbreviation, self.table_name)

