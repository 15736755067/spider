# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from pyquery import PyQuery
from ..items import SofangItem
from ..dao import db_module
from ..service import spider_service
class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['sofang.com']
    start_urls = ['http://sh.sofang.com/saleesb/area/aa2982']
    root_url = 'http://sh.sofang.com'
    table_name = 'worm_url_info_housing_sou'
    data_table = 'worm_housing_sofang'
    def parse(self, response):
        all_area = Selector(response=response).xpath('/html/body/div[4]/div[3]/div/dl[1]/dd[1]/a/@href').extract()
        for c_area in all_area:
            if c_area != '/saleesb/area/' and c_area != '/saleesb/area/aa2990' and c_area != '/saleesb/area/aa2989' and c_area != '/saleesb/area/aa2992' and c_area != '/saleesb/area/aa2985':
                n_area = self.root_url + c_area
                md5_area = self.md5(n_area)
                ret = spider_service.select_url(md5_area, self.table_name)
                if not ret:
                    spider_service.update_into(md5_area, self.table_name, c_area)
                    print(n_area)
                yield scrapy.Request(url=n_area, callback=self.parse)
        all_page = Selector(response=response).xpath('/html/body/div[4]/div[4]/div[1]/div[3]/ul/li/a/@href').extract()
        for c_page in all_page:
            n_page = self.root_url + c_page
            md5_url = self.md5(n_page)
            ret = spider_service.select_url(md5_url, self.table_name)
            if not ret:
                spider_service.update_into(md5_url, self.table_name, c_page)
            yield scrapy.Request(url=n_page, callback=self.parse)
        all_html = Selector(response=response).xpath('/html/body/div[4]/div[4]/div[1]/div[2]/dl/dd[1]/p/a/@href').extract()
        for c_html in all_html:
            n_html = self.root_url + c_html
            yield scrapy.Request(url=n_html, callback=self.parse_item)
    def parse_item(self, response):
        html = response.body

        ret = PyQuery(html).find('.real_detail')
        ret = PyQuery(ret).find('span')
        # for i in ret:
        #     print PyQuery(i).html()
        # address = PyQuery(ret[-1]).html()
        name = PyQuery(html).find('.conTop_title').children('h2').text()
        result = spider_service.select_url(name, self.data_table)
        if not result:
            address = PyQuery(ret[-1]).text()
            city_name = '上海市'
            listing_price = PyQuery(html).find('.price').text().split(' ')[0]
            district_name = PyQuery(ret[8]).text().strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '')
            built_up_area = PyQuery(ret[3]).text().split(' ')[0]
            floor_area = PyQuery(ret[4]).text().split(' ')[0]
            total_households = PyQuery(ret[5]).text().split(' ')[0]
            greening_rate = PyQuery(ret[6]).text().split(' ')[0]
            volume_ratio = PyQuery(ret[7]).text()
            property_fee = PyQuery(ret[11]).text().split(' ')[0]
            developers = PyQuery(ret[12]).text()
            property_company = PyQuery(ret[13]).text()
        # ret = PyQuery(html).find('.real_detail detail_tit').children('li span').text()
        # print ret
        # name = Selector(response=response).xpath(
        #     '/html/body/div[7]/div[3]/div[1]/div[2]/h2/text()').extract()
        # city_name = '上海市'
        #
        # address = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[15]/span/text()').extract()
        # listing_price = Selector(response=response).xpath(
        #     '/html/body/div[5]/div[3]/div[3]/div[2]/p/span/text()').extract()
        # district_name = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[9]/span/text()').extract()
        # build_up_area = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[4]/span/text()').extract()
        # floor_area = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[5]/span/text()').extract()
        # total_households = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[6]/span/text()').extract()
        # greening_rate = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[7]/span/text()').extract()
        # volume_ratio = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[8]/span/text()').extract()
        # property_fee = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[12]/span/text()').extract()
        # developers = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[13]/span/text()').extract()
        # property_company = Selector(response=response).xpath(
        #     '/html/body/div[8]/div[1]/div[1]/ul/li[14]/span/text()').extract()
            item_obj = SofangItem(name=name, city_name=city_name,
                                   built_up_area=built_up_area, floor_area=floor_area, total_households=total_households,
                                   greening_rate=greening_rate, volume_ratio=volume_ratio, district_name=district_name,
                                   property_fee=property_fee, developers=developers, property_company=property_company,
                                   address=address, listing_price=listing_price)
            yield item_obj

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(url)
        return obj.hexdigest()