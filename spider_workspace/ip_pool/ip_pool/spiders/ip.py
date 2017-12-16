# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import IpPoolItem
from scrapy import Selector
from pyquery import PyQuery
import requests
import json
from spider_service import spider_service
header = {
    "Accept": "text/html,application/json,text/javascript,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
}

class IpSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['www.data5u.com']

    table_name = 'ip_port'

    def start_requests(self):
        start_urls = ['http://www.data5u.com/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': '171.92.52.36:9000'})
    def parse(self, response):
        html = response.body
        all_ip = PyQuery(html).find('.l2')
        for c_ip in all_ip:
            ip = PyQuery(c_ip).find('li').eq(0).text()
            port = PyQuery(c_ip).find('li').eq(1).text()
            http_type = PyQuery(c_ip).find('li').eq(3).text()
            if  http_type == 'http':
                ip_port = 'http://' + ip + ':' + port
                requests.get(url='http://www.data5u.com/', proxies={'http': ip_port}).json()
                ret = spider_service.select_ip(ip_port, self.table_name)
                if not ret:
                    item = IpPoolItem(ip_port=ip_port)
                    yield item