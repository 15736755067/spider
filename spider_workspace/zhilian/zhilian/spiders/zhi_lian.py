# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from scrapy import Selector
from ..service import spider_service
import requests
from ..items import ZhilianItem


def create_page():
    li = []
    ''
    shenzhen = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&sm=0&fl=765&isadv=0&isfilter=1&pd=30&sg=9c334d799761429c976fd796c2db2e77'

    li.append(shenzhen)
    for i in range(2, 91):
        n_url = shenzhen + '&p={}'.format(i)
        li.append(n_url)
    guangzhou = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&isfilter=1&pd=30&sg=0e4f2c0a134f4012875afd859e04b3d6'
    li.append(guangzhou)
    for i in range(2, 91):
        n_url = guangzhou + '&p={}'.format(i)
        li.append(n_url)
    zhuhai = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E7%8F%A0%E6%B5%B7&isfilter=1&pd=30&sg=0775453d7f27466ba2e047966c649bd2'
    li.append(zhuhai)
    for i in range(2, 91):
        n_url = zhuhai + '&p={}'.format(i)
        li.append(n_url)

    zhongshan = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%AD%E5%B1%B1&isfilter=1&pd=30&sg=e99890fb77664f23a5e848185593643a'
    li.append(zhongshan)
    for i in range(2, 91):
        n_url = zhongshan + '&p={}'.format(i)
        li.append(n_url)
    foshan = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%BD%9B%E5%B1%B1&isfilter=1&pd=30&sg=1fed038232b548429a39e1ba18142173'
    li.append(foshan)
    for i in range(2, 91):
        n_url = foshan + '&p={}'.format(i)
        li.append(n_url)
    dongguan = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%9C%E8%8E%9E&isfilter=1&pd=30&sg=e10c6abc53c246309c1b225f562fc84e'
    li.append(dongguan)
    for i in range(2, 91):
        n_url = dongguan + '&p={}'.format(i)
        li.append(n_url)
    huizhou = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%83%A0%E5%B7%9E&isfilter=1&pd=30&sg=149a32e3e6e44d4188255b8fe8d61dff'
    li.append(huizhou)
    for i in range(2, 91):
        n_url = huizhou + '&p={}'.format(i)
        li.append(n_url)

    jiangmen = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B1%9F%E9%97%A8&isfilter=1&pd=30&sg=2991256829214addac346322314a3da6'
    li.append(jiangmen)
    for i in range(2, 91):
        n_url = jiangmen + '&p={}'.format(i)
        li.append(n_url)

    zhaoqing = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%82%87%E5%BA%86&isfilter=1&pd=30&sg=6ccd3747ad114d938b0d2c61edcfc2ff'
    li.append(zhaoqing)
    for i in range(2, 91):
        n_url = zhaoqing + '&p={}'.format(i)
        li.append(n_url)
    hongkong = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%A6%99%E6%B8%AF&isfilter=1&pd=30&sg=379b150a8d2f4402b48391c507fd78fa'
    li.append(hongkong)
    for i in range(2, 16):
        n_url = hongkong + '&p={}'.format(i)
        li.append(n_url)
    aomen = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%BE%B3%E9%97%A8&isfilter=1&pd=30&sg=9f83b576068d4d4cb51031d9db9b5ad5'
    li.append(aomen)
    for i in range(2, 10):
        n_url = aomen + '&p={}'.format(i)
        li.append(n_url)
    return li


class ZhiLianSpider(scrapy.Spider):
    name = 'zhi_lian'
    allowed_domains = ['zhaopin.com']
    start_urls = create_page()
    table_name = u'worm_url_info_zhilian'
    company_name_old = u'worm_zhaopin_company'
    def parse(self, response):
        all_page = Selector(response=response).xpath(
            '/html/body/div[3]/div[3]/div[3]/form/div[1]/div[1]/div[3]/ul/li/a/@href').extract()
        for c_page in all_page:
            yield scrapy.Request(url=c_page, callback=self.parse1)

    def parse1(self, response):
        city = Selector(response=response).xpath('//*[@id="JobLocation"]/@value').extract()[0]
        html = response.body
        table_list = PyQuery(html).find('#newlist_list_content_table').find('table')
        for i in range(1, len(table_list)):
            company_name = PyQuery(table_list[i]).find('td').eq(2).find('a').text()
            ret = spider_service.select_url(city=city, company_name=company_name, table_name=self.company_name_old)
            if not ret:
                url = PyQuery(table_list[i]).find('td').eq(0).find('a').attr('href')
                yield scrapy.Request(url=url, meta={'item': city}, callback=self.parse_item)
    def parse_item(self, response):
        city = response.meta.get('item')
        html = response.body
        name = PyQuery(html).find('.company-name-t').find('a').text()
        size = PyQuery(html).find('.terminal-company').find('li').eq(0).find('strong').text()
        nature = PyQuery(html).find('.terminal-company').find('li').eq(1).find('strong').text()
        industry = PyQuery(html).find('.terminal-company').find('li').eq(2).find('a').text()
        website = PyQuery(html).find('.terminal-company').find('li').eq(-2).find('a').text()
        if not website.startswith('www'):
            website = None
        address = PyQuery(html).find('.terminal-company').find('li').eq(-1).find('strong').text().strip()
        item = ZhilianItem(city=city, name=name, size=size, nature=nature, industry=industry, website=website, address=address)
        yield item
            # def parse(self, response):
            #     # print response.body
            #     # all_page = Selector(response=response).xpath('/html/body/div[3]/div[3]/div[3]/form/div[1]/div[1]/div[3]/ul/li/a/@href').extract()
            #     # for c_page in all_page:
            #     #     md5_url = self.md5(c_page)
            #     #     ret = spider_service.select_url(md5_url, self.table_name)
            #     #     if not ret:
            #     #         print c_page
            #     #         spider_service.update_into(md5_url, self.table_name)
            #     #         yield scrapy.Request(url=c_page, callback=self.parse)
            #     yield scrapy.Request(url=response.url, callback=self.parse_item)
            # def parse_item(self, response):
            #     city = Selector(response=response).xpath('//*[@id="JobLocation"]/@value').extract()[0]
            #     html = response.body
            #     table_list = PyQuery(html).find('#newlist_list_content_table').find('table')
            #     for i in range(len(table_list)):
            #         job_name = PyQuery(table_list[i + 1]).find('td').eq(0).find('a').text()
            #         feedback_rate = PyQuery(table_list[i + 1]).find('td').eq(1).find('span').text()
            #         company_name = PyQuery(table_list[i + 1]).find('td').eq(2).find('a').text()
            #         salary = PyQuery(table_list[i + 1]).find('td').eq(3).text()
            #         place = PyQuery(table_list[i + 1]).find('td').eq(4).text()
            #         release_date = PyQuery(table_list[i + 1]).find('td').eq(5).find('span').text()
            #         job_url = PyQuery(table_list[i + 1]).find('td').eq(0).find('a').attr('href')
            #         job_content = requests.get(job_url)
            #         job_content = job_content.text
            #         job_type = PyQuery(job_content).find('.terminal-ul').find('li').eq(7).find('a').text()
            #         numbers = PyQuery(job_content).find('.terminal-ul').find('li').eq(6).find('strong').text()
            #         education = PyQuery(job_content).find('.terminal-ul').find('li').eq(5).find('strong').text()
            #         ret = spider_service.select_url(city, job_name, company_name, self.table_name)
            #         if not ret:
            # c_page_table = Selector(response=response).xpath('//*[@id="newlist_list_content_table"]/table').extract()
            # for i in range(len(c_page_table)):
            # city = Selector(response=response).xpath(
            #     '//*[@id="JobLocation"]/@value').extract()
            # job_name = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[1]/div/a/text()'.format(i + 1)).extract()
            # job_url = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[1]/div/a/@href'.format(i + 1)).extract()
            # company_name = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[3]/a[1]/text()'.format(i + 1)).extract()
            # place = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[5]/text()'.format(i + 1)).extract()
            # salary = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[4]/text()'.format(i + 1)).extract()
            # release_date = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[6]/span/text()'.format(i + 1)).extract()
            # feedback_rate = Selector(response=response).xpath(
            #     '//*[@id="newlist_list_content_table"]/table[{}]/tbody/tr[1]/td[2]/span/text()'.format(i + 1)).extract()
            # html = requests.get(url=job_url)
            # html =html.text
            # job_type = Selector(text=html).xpath('/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()').extract()
            # numbers = Selector(text=html).xpath('/html/body/div[6]/div[1]/ul/li[7]/strong/text()').extract()
            # education = Selector(text=html).xpath('/html/body/div[6]/div[1]/ul/li[6]/strong/text()').extract()
        # item = ZhilianItem(city=city, job_name=job_name, company_name=company_name, place=place, salary=salary,
        #                    release_date=release_date, feedback_rate=feedback_rate, job_type=job_type,
        #                    numbers=numbers, education=education)
        # yield item


    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(url)
        return obj.hexdigest()
