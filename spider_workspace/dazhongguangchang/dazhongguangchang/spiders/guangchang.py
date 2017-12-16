# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from ..header.create_header import *
from ..items import DazhongguangchangItem
from pyquery import PyQuery
from ..service import spider_service
from config import create_url, create_sleep
import time


# print "请输入城市id"
# key = int(raw_input())
class GuangchangSpider(scrapy.Spider):
    name = 'guangchang'
    allowed_domains = ['www.dianping.com']
    start_urls = create_url()
    table_name = 's04_dianping_plaze_info'

    def parse(self, response):
        """
        解析初始页面
        :param response:
        :return:
        """
        try:
            city_name = Selector(response).xpath('//*[@id="logo-input"]/div/a[2]/span/text()').extract()[0]
        except:
            city_name = None
        all_area_url = Selector(response).xpath('//*[@id="region-nav"]/a/@href').extract()
        all_area = Selector(response).xpath('//*[@id="region-nav"]/a/span/text()').extract()
        for i in range(len(all_area_url)):
            area_url = all_area_url[i]
            adname = all_area[i]
            create_sleep()
            yield scrapy.Request(url=area_url, meta={"city_name": city_name, "adname": adname},
                                 callback=self.parse_page, headers=header)

    def parse_page(self, response):
        """
        解析页码
        :param response:
        :return:
        """
        city_name = response.meta.get('city_name')
        adname = response.meta.get('adname')
        end_page = PyQuery(response.body).find('.page').find('a').eq(-2).attr('href')
        dic = {"city_name": city_name, "adname": adname}
        if end_page:
            num = end_page.split('/')[-1].split('p')[-1]
            try:
                c_num, aid = num.split('?')
            except:
                c_num = num
                aid = ""
            head, head1, mid, end = end_page.split('p')

            for c_page in range(1, int(c_num) + 1):
                if aid == '':
                    n_page = head + 'p' + head1 + 'p' + mid + 'p{}'.format(c_page)
                else:
                    n_page = head + 'p' + head1 + 'p' + mid + 'p{}'.format(c_page) + '?' + aid
                create_sleep()
                yield scrapy.Request(url=n_page, meta=dic, callback=self.parse_area, headers=header1)
        else:
            create_sleep()
            yield scrapy.Request(url=response.url, meta=dic, callback=self.parse_area, headers=header1)

    def parse_area(self, response):
        """
        解析行政区页面
        :param response:
        :return:
        """

        city_name = response.meta.get('city_name')
        adname = response.meta.get('adname')
        type = Selector(response).xpath('//*[@id="classfy"]/a[@class="cur"]/span/text()').extract()[0]
        all_store_url = Selector(response).xpath(
            '//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href').extract()
        all_comments_count = Selector(response).xpath(
            '//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/a[1]')
        all_comments_count_list = []
        for comments_count_i in all_comments_count:
            try:
                comments_count = comments_count_i.xpath('./b/text()').extract()[0]
            except:
                comments_count = None
            all_comments_count_list.append(comments_count)
        all_address = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[3]')
        all_address_list = []
        for c_address in all_address:
            try:
                cc_address = c_address.xpath('./span/text()').extract()[0]
            except:
                cc_address = None
            all_address_list.append(cc_address)
        all_consumption_amt = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/a[2]')
        all_consumption_amt_list = []
        for c_consumption_amt in all_consumption_amt:
            try:
                cc_consumption_amt = c_consumption_amt.xpath('./b/text()').extract()[0].split('￥')[-1]
            except:
                cc_consumption_amt = None
            all_consumption_amt_list.append(cc_consumption_amt)
        all_business_district = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[3]/a[2]')
        all_business_district_list = []
        for c_business_district in all_business_district:
            try:
                cc_business_district = c_business_district.xpath('./span/text()').extract()[0]
            except:
                cc_business_district = None
            all_business_district_list.append(cc_business_district)
        all_place_name = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a')
        all_place_name_list = []
        for c_place_name in all_place_name:
            try:
                cc_place_name = c_place_name.xpath('./h4/text()').extract()[0]
            except:
                cc_place_name = None
            all_place_name_list.append(cc_place_name)
        all_star = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]')
        all_star_list = []
        for c_star in all_star:
            try:
                cc_star = c_star.xpath('./span/@title').extract()[0]
            except:
                cc_star = "该商户暂无星级"
            all_star_list.append(cc_star)
        all_con = Selector(response).xpath('//*[@id="shop-all-list"]/ul/li/div[@class="txt"]')
        all_quality_list = []
        all_environment_list = []
        all_service_list = []
        for c_con in all_con:
            try:
                c_quality = c_con.xpath('./span[@class="comment-list"]/span[1]/b/text()').extract()[0]
            except:
                c_quality = ""
            all_quality_list.append(c_quality)
            try:
                c_environment = c_con.xpath('./span[@class="comment-list"]/span[2]/b/text()').extract()[0]
            except:
                c_environment = ""
            all_environment_list.append(c_environment)
            try:
                c_service = c_con.xpath('./span[@class="comment-list"]/span[3]/b/text()').extract()[0]
            except:
                c_service = ""
            all_service_list.append(c_service)
        for i in range(len(all_store_url)):
            c_store_url = all_store_url[i]
            id = c_store_url.split('/')[-1]
            ret = spider_service.select_id(id, self.table_name)
            c_comments_count = all_comments_count_list[i]
            address = all_address_list[i]
            consumption_amt = all_consumption_amt_list[i]
            business_district = all_business_district_list[i]
            place_name = all_place_name_list[i]
            star = all_star_list[i]
            quality = all_quality_list[i]
            environment = all_environment_list[i]
            service = all_service_list[i]
            dic = {"city_name": city_name, "adname": adname, "comments_count": c_comments_count, "execute": ret,
                   "type": type, "address": address, "consumption_amt": consumption_amt, "id": id,
                   "business_district": business_district, "place_name": place_name, "star": star, "quality": quality,
                   "environment": environment, "service": service}
            create_sleep()
            if ret:
                # item = DazhongguangchangItem(dic=dic)
                # yield item
                yield scrapy.Request(url=c_store_url, meta=dic, callback=self.parse_store, headers=header4)
            else:
                pass

    def parse_store(self, response):
        """
        解析商铺页面
        :param response:
        :return:
        """
        star = response.meta.get('star')
        place_name = response.meta.get('place_name')
        business_district = response.meta.get('business_district')
        address = response.meta.get('address')
        consumption_amt = response.meta.get('consumption_amt')
        type = response.meta.get('type')
        execute = response.meta.get('execute')
        city_name = response.meta.get('city_name')
        adname = response.meta.get('adname')
        comments_count = response.meta.get('comments_count')
        id = response.url.split('/')[-1]
        quality = response.meta.get('quality')
        environment = response.meta.get('environment')
        service = response.meta.get('service')
        # place_name = Selector(response).xpath('//*[@id="top"]/div[6]/div[2]/div[1]/div[2]/h2/text()').extract()[0]
        # try:
        #     star = Selector(response).xpath('//*[@id="basic-info"]/div[1]/span[1]/@title').extract()[0]
        #
        # except:
        #     star = None
        # if not star:
        #     try:
        #         star = Selector(response).xpath(
        #             '//*[@id="market-detail"]/div/p[2]/span[2]/@class').extract()[0].split('str')[-1].split(' ')[0]
        #     except:
        #         star = None
        #     if not star:
        #         if star == '10':
        #             star = "一星商户"
        #         elif star == '20':
        #             star = "二星商户"
        #         elif star == '30':
        #             star = "三星商户"
        #         elif star == '35':
        #             star = "准四星商户"
        #         elif star == '40':
        #             star = "四星商户"
        #         elif star == '45':
        #             star = "准五星商户"
        #         elif star == '50':
        #             star = "五星商户"
        #         else:
        #             star = "该商户暂无星级"
        try:
            five_star_comments_count = Selector(response).xpath(
                '//*[@id="comment"]/h2/span/a[2]/span/text()').extract()[0].split('(')[-1].split(')')[0]
        except:
            five_star_comments_count = 0
        try:
            four_star_comments_count = Selector(response).xpath(
                '//*[@id="comment"]/h2/span/a[3]/span/text()').extract()[0].split('(')[-1].split(')')[0]
        except:
            four_star_comments_count = 0
        try:
            three_star_comments_count = Selector(response).xpath(
                '//*[@id="comment"]/h2/span/a[4]/span/text()').extract()[0].split('(')[-1].split(')')[0]
        except:
            three_star_comments_count = 0
        try:
            two_star_comments_count = Selector(response).xpath(
                '//*[@id="comment"]/h2/span/a[5]/span/text()').extract()[0].split('(')[-1].split(')')[0]
        except:
            two_star_comments_count = 0
        try:
            one_star_comments_count = Selector(response).xpath(
                '//*[@id="comment"]/h2/span/a[6]/span/text()').extract()[0].split('(')[-1].split(')')[0]
        except:
            one_star_comments_count = 0

        # try:
        #     quality = Selector(response).xpath(
        #         '//*[@id="market-detail"]/div/p[2]/span[3]/text()').extract()[0].split('产品')[-1]
        # except:
        #     quality = None
        # if not quality:
        #     try:
        #         quality = Selector(response).xpath(
        #             '//*[@id="comment_score"]/span[1]/text()').extract()[0].split('：')[-1]
        #     except:
        #         quality = None
        # try:
        #     environment = Selector(response).xpath(
        #         '//*[@id="market-detail"]/div/p[2]/span[4]/text()').extract()[0].split('环境')[-1]
        # except:
        #     environment = None
        # if not environment:
        #     try:
        #         environment = Selector(response).xpath(
        #             '//*[@id="comment_score"]/span[2]/text()').extract()[0].split('：')[-1]
        #     except:
        #         environment = None
        # try:
        #     service = Selector(response).xpath(
        #         '//*[@id="market-detail"]/div/p[2]/span[5]/text()').extract()[0].split('服务')[-1]
        # except:
        #     service = None
        # if not service:
        #     try:
        #         service = Selector(response).xpath(
        #             '//*[@id="comment_score"]/span[3]/text()').extract()[0].split('：')[-1]
        #     except:
        #         service = None
        dic = {"execute": execute, "city_name": city_name, "adname": adname, "id": id,
               "comments_count": comments_count,
               "place_name": place_name, "five_star_comments_count": five_star_comments_count, "star": star,
               "four_star_comments_count": four_star_comments_count,
               "three_star_comments_count": three_star_comments_count,
               "two_star_comments_count": two_star_comments_count,
               "one_star_comments_count": one_star_comments_count,
               "consumption_amt": consumption_amt, "type": type,
               "business_district": business_district, "address": address, "quality": quality,
               "environment": environment, "service": service}
        item = DazhongguangchangItem(dic=dic)
        yield item



class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1/']

    def parse(self, response):
        print response.body