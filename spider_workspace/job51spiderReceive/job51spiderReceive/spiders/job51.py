# -*- coding: utf-8 -*-
import scrapy
import redis
from config import create_sleep
from ..items import Job51SpiderreceiveItem

def get_area_url():
    """
    通过redis获取url
    :return:
    """
    pool = redis.ConnectionPool(host='192.168.0.5', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    start_url = r.brpop('job51', 0)
    return [start_url[1]]


class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = []
    start_urls = get_area_url()

    def parse(self, response):
        """
        开始
        :param response:
        :return:
        """
        city = response.xpath('/html/body/div[2]/div[3]/div/p/text()').extract()[0]
        all_company = response.xpath('//*[@id="resultList"]/div/span[1]/a/@href').extract()
        for c_company in all_company:
            create_sleep()
            yield scrapy.Request(url=c_company, meta={'city': city}, callback=self.parse_company)

    def parse_company(self, response):
        """
        解析company页面
        :param response:
        :return:
        """
        city = response.meta.get('city')
        name = response.xpath('/html/body/div[2]/div[2]/div[2]/div/h1/text()').extract()[0]
        nature, size, industry = response.xpath('/html/body/div[2]/div[2]/div[2]/div/p[1]/text()').extract()[0].split(
            '|')
        nature = nature.strip()
        size = size.strip()
        industry = industry.strip()
        try:

            website = response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div/p[2]/a/text()').extract()[0]
        except:
            website = None
        try:
            address = response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div/p[1]').extract()[0].split('</span>')[-1].split(' ')[0]
        except:
            address = None
        dic = {'city': city, 'name': name, 'nature': nature, 'size': size, 'industry': industry, 'website': website,
               'address': address}
        item = Job51SpiderreceiveItem(dic=dic)
        yield item