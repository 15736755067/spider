# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from ..items import XicidailiItem
from ..test_proxy import test_proxy
import time


def create_page():
    li = []
    url = 'http://www.xicidaili.com/nn/{}'
    for i in range(1, 100):
        n_url = url.format(i)
        li.append(n_url)
    return li


class DailiSpider(scrapy.Spider):
    name = 'daili'
    allowed_domains = ['www.xicidaili.com']
    start_urls = create_page()

    def parse(self, response):
        time.sleep(3)
        all_content = Selector(response).xpath('//tr[@class="odd"]')
        for c_content in all_content:
            time.sleep(3)
            keep_live = c_content.xpath('./td[9]/text()').extract()[0]
            sudu = c_content.xpath('./td[7]/div/@title').extract()[0].split('秒')[0]
            connect_time = c_content.xpath('./td[8]/div/@title').extract()[0].split('秒')[0]
            if float(sudu) < 2 and float(connect_time) < 2:
                # if int(keep_live.split('天')[0]) > 100:
                c_ip = c_content.xpath('./td[2]/text()').extract()[0]
                c_port = c_content.xpath('./td[3]/text()').extract()[0]
                ip_type = c_content.xpath('./td[6]/text()').extract()[0].lower()
                ip_port = ip_type + "://" + c_ip + ":" + c_port
                obj = test_proxy.TestProxy(ip_port)
                ret = obj.run()
                if ret:
                    item = XicidailiItem(ip_port=ip_port)
                    yield item
