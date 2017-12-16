# -*- coding: utf-8 -*-
import scrapy
import time
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
        self.browser = webdriver.Chrome()
    def parse(self, response):
        """
        开始
        :param response:
        :return:
        """
        login_url = response.url
        self.login(login_url)
        self.brower_get()
        tag_province = '//*[@class="data-list"]/ul/li[{}]/a'
        html = self.browser.page_source
        all_num_tag_province = len(Selector(text=html).xpath('//*[@class="data-list"]/ul/li/a').extract())
        for i in range(1, all_num_tag_province + 1):
            self.brower_get()
            c_tag_province = tag_province.format(i)
            n_tag_province = self.browser.find_element_by_xpath(c_tag_province)
            webdriver.ActionChains(self.browser).move_to_element(n_tag_province).click().perform()
            create_sleep()
            c_html = self.browser.page_source
            tag_city = '//*[@class="data-list"]/ul/li[{}]/a'
            all_num_tag_city = len(Selector(text=c_html).xpath('//*[@class="data-list"]/ul/li/a').extract())
            for k in range(1, all_num_tag_city + 1):
                self.brower_get()
                create_sleep()
                cc_tag_province = self.browser.find_element_by_xpath(c_tag_province)
                webdriver.ActionChains(self.browser).move_to_element(cc_tag_province).perform()
                create_sleep()
                webdriver.ActionChains(self.browser).move_to_element(cc_tag_province).click().perform()
                create_sleep()
                c_tag_city = tag_city.format(k)
                c_tag_city = self.browser.find_element_by_xpath(c_tag_city)
                webdriver.ActionChains(self.browser).move_to_element(c_tag_city).perform()
                create_sleep()
                webdriver.ActionChains(self.browser).move_to_element(c_tag_city).click().perform()
                create_sleep()
                self.browser.find_element_by_xpath('//*[@id="sojob"]/div[10]/div[3]/a[2]').click()
                create_sleep()
                city_html = self.browser.page_source
                key_tag = Selector(text=city_html).xpath(
                    '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl/dt/text()').extract()
                if key_tag[3] =='地区：':
                    all_num_tag_area = len(Selector(text=city_html).xpath(
                        '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[4]/dd/a').extract())
                elif key_tag[2] == '地区：':
                    tag_area = '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[{}]'
                    all_num_tag_area = len(Selector(text=city_html).xpath(
                        '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a').extract())
                else:
                    self.click_end_page()
                    self.parse_page()
                    continue
                for m in range(1, all_num_tag_area + 1):
                    c_area_html = self.browser.page_source
                    c_key_tag = Selector(text=c_area_html).xpath(
                        '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl/dt/text()').extract()
                    if c_key_tag[3] == '地区：':
                        try:
                            tag_area = '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[4]/dd/a[{}]'
                            c_tag_area = tag_area.format(m)
                            n_tag_area = self.browser.find_element_by_xpath(c_tag_area)
                        except:
                            tag_area = '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[{}]'
                            c_tag_area = tag_area.format(m)
                            n_tag_area = self.browser.find_element_by_xpath(c_tag_area)
                    elif c_key_tag[2] == '地区：':
                        try:
                            tag_area = '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[{}]'
                            c_tag_area = tag_area.format(m)
                            n_tag_area = self.browser.find_element_by_xpath(c_tag_area)
                        except:
                            tag_area = '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[4]/dd/a[{}]'
                            c_tag_area = tag_area.format(m)
                            n_tag_area = self.browser.find_element_by_xpath(c_tag_area)
                            '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[12]'
                    webdriver.ActionChains(self.browser).move_to_element(n_tag_area).click().perform()
                    create_sleep()
                    self.click_end_page()
                    self.parse_page()
    def brower_get(self):
        """
        进入特定的url页面
        :return:
        """
        self.browser.get('https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar&init=1')
        create_sleep()
        try:
            WebDriverWait(self.browser, 10).until(lambda the_brower: the_brower.find_element_by_xpath(
                '//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[14]'))
        except:
            pass
        other = self.browser.find_element_by_xpath('//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[3]/dd/a[14]')
        webdriver.ActionChains(self.browser).move_to_element(other).click().perform()
        create_sleep()
    def login(self, url):
        """
        登录
        :param url:
        :return:
        """
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[2]/div[5]/p/a').click()
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/div[1]/input').send_keys(
            '15736755067')
        create_sleep()
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/div[2]/input').send_keys(
            'taochen123')
        create_sleep()
        self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[1]/div[2]/div/form[1]/input[3]').click()
        create_sleep()
    def parse_page(self):
        """
        通过最大页url,生成所有url
        :return:
        """
        try:
            page_url, max_page = self.browser.current_url.split('curPage=')
            for n in range(int(max_page) + 1):
                c_page_url = page_url + 'curPage={}'.format(n)
                r.lpush('liepin', c_page_url)
        except:
            page_url = self.browser.current_url
            r.lpush('liepin', page_url)

    def click_end_page(self):
        """
        跳转到末尾页
        :return:
        """
        area_html = self.browser.page_source
        tag_page = '//*[@id="sojob"]/div[2]/div/div[1]/div[1]/div/div/a[{}]'
        c_page_num = len(Selector(text=area_html).xpath('//*[@id="sojob"]/div[2]/div/div[1]/div[1]/div/div/a'))
        c_tag_page = tag_page.format(c_page_num)
        n_tag_page = self.browser.find_element_by_xpath(c_tag_page)
        webdriver.ActionChains(self.browser).move_to_element(n_tag_page).perform()
        create_sleep()
        webdriver.ActionChains(self.browser).move_to_element(n_tag_page).click().perform()
        create_sleep()