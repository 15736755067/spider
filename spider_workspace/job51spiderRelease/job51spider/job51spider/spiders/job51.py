# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import redis
pool = redis.ConnectionPool(host='192.168.0.5', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['www.51job.com']
    start_urls = ['http://www.51job.com/']
    def __init__(self):
        self.brower = webdriver.Chrome()
    def parse(self, response):
        """
        开始
        :param response:
        :return:
        """
        all_area = response.xpath('//*[@id="area_channel_layer_all"]/div/span/a/@href').extract()
        for c_area in all_area:
            time.sleep(3)
            yield scrapy.Request(url=c_area, callback=self.parse_area)

    def parse_area(self, response):
        """
        获取页面url,添加到redis队列
        :param response:
        :return:
        """
        self.brower.get(response.url)
        self.brower.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/button').click()

        WebDriverWait(self.brower, 10).until(lambda the_brower: the_brower.find_element_by_xpath('//*[@id="funtype_input"]').is_displayed())
        html = self.brower.page_source


        max_page = Selector(text=html).xpath(
            '//*[@id="resultList"]/div[54]/div/div/div/span[1]/text()').extract()[0].split('页')[0].split('共')[1]
        page_url = Selector(text=html).xpath('//*[@id="resultList"]/div[54]/div/div/div/ul/li/a/@href').extract()[-2]
        page_num = Selector(text=html).xpath('//*[@id="resultList"]/div[54]/div/div/div/ul/li/a/text()').extract()[-2]
        num = len(page_num)
        head, end = page_url.split('.html')
        n_head = head[: -num]
        for i in range(1, int(max_page) + 1):
            c_page = n_head + '{}.html'.format(i) + end
            r.lpush('job51', c_page)
