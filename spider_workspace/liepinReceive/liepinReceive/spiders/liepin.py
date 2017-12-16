# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import LiepinreceiveItem
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from config import create_sleep
import redis
pool = redis.ConnectionPool(host='192.168.0.5', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']
    header_url = 'https://www.liepin.com'

    def __init__(self):

        self.browser = webdriver.Chrome() #生成浏览器对象
        dispatcher.connect(self.spider_stoped, signals.spider_closed) #绑定信号&方法

    def spider_stoped(self):
        self.browser.quit()
    def parse(self, response):
        """
        通过redis获取页面url,解析页面获取company信息
        :param response:
        :return:
        """
        login_url = response.url
        self.login(login_url)
        url = r.brpop('liepin', 0)[1]
        self.browser.get(url)
        create_sleep()
        try:
            WebDriverWait(self.browser, 10).until(lambda the_brower: the_brower.find_element_by_xpath(
                '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li/div/div[1]/h3/a'))
        except:
            pass
        c_page_html = self.browser.page_source
        all_job_url = Selector(text=c_page_html).xpath(
            '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li/div/div[1]/h3/a/@href').extract()

        for c_job_url in all_job_url:
            if c_job_url.startswith('http'):
                self.browser.get(c_job_url)
            else:
                n_job_url = 'https://www.liepin.com' + c_job_url
                self.browser.get(n_job_url)
            create_sleep()
            try:
                WebDriverWait(self.browser, 10).until(lambda the_browser: the_browser.find_element_by_xpath(
                    '//*[@class="job-qualifications"]/span'))
            except:
                pass
            company_html = self.browser.page_source
            try:
                city = Selector(text=company_html).xpath(
                    '//*[@class="basic-infor"]/span/a/text()').extract()[0]
            except:
                city = Selector(text=company_html).xpath(
                    '//*[@class="basic-infor"]/span').extract()[0].split('</i>')[-1].split('</span>')[0].strip()
            if city:
                try:
                    city = city.split('-')[0]
                except:
                    pass
            try:
                name = Selector(text=company_html).xpath(
                    '//*[@class="company-logo"]/p/a/text()').extract()[0]
            except:
                name = Selector(text=company_html).xpath('//*[@class="company-name"]/text()').extract()[0]
            try:
                size = Selector(text=company_html).xpath(
                    '//*[@class="new-compintro"]/li[2]/text()').extract()[0].split('：')[-1]
            except:
                try:
                    size = Selector(text=company_html).xpath(
                        '//*[@id="job-hunter"]/div[1]/div[1]/div[1]/div[1]/div/div[4]/div/ul/li[6]').extract()[0].split(
                        '</span>')[-1].split('</li>')[0]
                except:
                    size = None
            try:
                nature = Selector(text=company_html).xpath(
                    '//*[@id="job-hunter"]/div[1]/div[1]/div[1]/div[1]/div/div[4]/div/ul/li[5]').extract()[0].split(
                        '</span>')[-1].split('</li>')[0]
            except:
                nature = None
            try:
                industry = Selector(text=company_html).xpath(
                    '//*[@class="new-compintro"]/li[1]/a/text()').extract()[0]
            except:
                try:
                    industry = Selector(text=company_html).xpath(
                        '//*[@class="new-compintro"]/li[1]/text()').extract()[0].split('：')[-1]
                except:
                    try:
                        industry = Selector(text=company_html).xpath(
                            '//*[@id="job-hunter"]/div[1]/div[1]/div[1]/div[1]/div/div[4]/div/ul/li[3]/a/@title').extract()[
                            0]
                    except:
                        industry = None
            # website
            try:
                address = Selector(text=company_html).xpath(
                    '//*[@class="new-compintro"]/li[3]/text()').extract()[0].split('：')[-1]
            except:
                address = None
            # job_qualifications = Selector(text=company_html).xpath(
            #     '//*[@class="job-qualifications"]/span/text()').extract()
            # all_job_qualifications = ''
            # for c_job_qualification in job_qualifications:
            #     all_job_qualifications = all_job_qualifications + '|' + c_job_qualification
            dic = {'city': city, 'name': name, 'nature': nature, 'size': size, 'industry': industry, 'address': address,
                   }
            item = LiepinreceiveItem(dic=dic)
            yield item

    # def browser_get(self, url):
    #     self.browser.get(url)
    #     WebDriverWait(self.browser, 10).until(lambda the_brower: the_brower.find_element_by_xpath(
    #         '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li/div/div[1]/h3/a'))
    #     c_page_html = self.browser.page_source
    #     all_num_job = len(Selector(text=c_page_html).xpath(
    #         '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li/div/div[1]/h3/a').extract())
    #     tag_job = '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li[{}]/div/div[1]/h3/a'
    #     for i in range(1, all_num_job + 1):
    #         self.browser.get(url)
    #         c_tag_job = tag_job.format(i)
    #         cc_tag_job = self.browser.find_element_by_xpath(c_tag_job)
    #         webdriver.ActionChains(self.browser).move_to_element(cc_tag_job).perform()
    #         time.sleep(3)
    #         webdriver.ActionChains(self.browser).move_to_element(cc_tag_job).click().perform()
    #         time.sleep(3)
    #         # self.parse_company()
    #         # def parse_company(self):
    #         company_html = self.browser.page_source
    #         city = Selector(text=company_html).xpath(
    #             '//*[@class="basic-infor"]/span/a/text()').extract()[0]
    #         name = Selector(text=company_html).xpath(
    #             '//*[@class="company-logo"]/p/a/text()').extract()[0]
    #         size = Selector(text=company_html).xpath(
    #             '//*[@class="new-compintro"]/li[2]/text()').extract()[0].split('：')[-1]
    #         # nature = Selector(text=company_html).xpath('//*[@class="new-compintro"]/li[2]/text()')
    #         industry = Selector(text=company_html).xpath(
    #             '//*[@class="new-compintro"]/li[1]/text()').extract()[0].split('：')[-1]
    #         # website
    #         address = Selector(text=company_html).xpath(
    #             '//*[@class="new-compintro"]/li[3]/text()').extract()[0].split('：')[-1]
    #         job_qualifications = Selector(text=company_html).xpath('//*[@class="job-qualifications"]/text()').extract()[
    #             0]
    #         dic = {'city': city, 'name': name, 'size': size, 'industry': industry, 'address': address,
    #                'job_qualifications': job_qualifications}
    #         item = LiepinreceiveItem(dic=dic)
    #         yield item
    def login(self, url):
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[2]/div[5]/p/a').click()
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/div[1]/input').send_keys(
            '15736755067')
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/div[2]/input').send_keys(
            'taochen123')
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/input[3]').click()
        time.sleep(2)
        # def parse_page(self, url):
        #     c_page_html = self.browser.page_source
        #     all_num_job = len(Selector(text=c_page_html).xpath(
        #         '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li/div/div[1]/h3/a').extract())
        #     tag_job = '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li[{}]/div/div[1]/h3/a'
        #     for i in range(1, all_num_job + 1):
        #         self.browser_get(url)
        #         c_tag_job = tag_job.format(i)
        #         cc_tag_job = self.browser.find_element_by_xpath(c_tag_job)
        #         webdriver.ActionChains(self.browser).move_to_element(cc_tag_job).perform()
        #         time.sleep(3)
        #         webdriver.ActionChains(self.browser).move_to_element(cc_tag_job).click().perform()
        #         time.sleep(3)
        #         # self.parse_company()
        # # def parse_company(self):
        #         company_html = self.browser.page_source
        #         city = Selector(text=company_html).xpath(
        #             '//*[@class="basic-infor"]/span/a/text()').extract()[0]
        #         name = Selector(text=company_html).xpath(
        #             '//*[@class="company-logo"]/p/a/text()').extract()[0]
        #         size = Selector(text=company_html).xpath(
        #             '//*[@class="new-compintro"]/li[2]/text()').extract()[0].split('：')[-1]
        #         # nature = Selector(text=company_html).xpath('//*[@class="new-compintro"]/li[2]/text()')
        #         industry = Selector(text=company_html).xpath(
        #             '//*[@class="new-compintro"]/li[1]/text()').extract()[0].split('：')[-1]
        #         # website
        #         address = Selector(text=company_html).xpath(
        #             '//*[@class="new-compintro"]/li[3]/text()').extract()[0].split('：')[-1]
        #         job_qualifications = Selector(text=company_html).xpath('//*[@class="job-qualifications"]/text()').extract()[0]
        #         dic = {'city': city, 'name': name, 'size': size, 'industry': industry, 'address': address,
        #                'job_qualifications': job_qualifications}
        #         item = LiepinreceiveItem(dic=dic)
        #         yield item
