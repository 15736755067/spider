# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from pyquery import PyQuery
from zhongchou.items import ZhongchouItem
from zhongchou.service import spider_service


class ZhongSpider(scrapy.Spider):
    name = 'zhong'
    allowed_domains = ['zhongchou.com']
    # start_urls = ['http://www.zhongchou.com/browse/di',
    #               'http://www.zhongchou.com/browse/di-p2',
    #               'http://www.zhongchou.com/browse/di-p3',
    #               'http://www.zhongchou.com/browse/di-p4',
    #               'http://www.zhongchou.com/browse/di-p5',
    #               'http://www.zhongchou.com/browse/di-p6',
    #               'http://www.zhongchou.com/browse/di-p7',
    #               'http://www.zhongchou.com/browse/di-p8',
    #               'http://www.zhongchou.com/browse/di-p9',
    #               'http://www.zhongchou.com/browse/di-p10',
    #               'http://www.zhongchou.com/browse/di-p11',
    #               'http://www.zhongchou.com/browse/di-p12',
    #               'http://www.zhongchou.com/browse/di-p13',
    #               'http://www.zhongchou.com/browse/di-p14']
    start_urls = ['http://www.zhongchou.com/browse/re']

    table_name = u'worm_url_info_zhong_chou'
    def parse(self, response):
        c_url = response.url
        yield scrapy.Request(url=c_url, callback=self.parse_item)
        # # all_url = Selector(response=response).xpath(
        # #     '//*[@id="ng-app"]/body/div[5]/div/div/div[2]/div/a/@href').extract()
        # # for c_url in all_url:
        # #     if c_url != u'http://www.zhongchou.com/browse/si_c':
        # #         md5_url = self.md5(c_url)
        # #         ret = spider_service.select_url(md5_url, self.table_name)
        # #         if not ret:
        # #             spider_service.update_into(md5_url, self.table_name)
        # #             yield scrapy.Request(url=c_url, callback=self.parse)
        #
        # c_all_page = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[7]/div/div/a/@href').extract()
        # for c_page in c_all_page:
        #     md5_page = self.md5(c_page)
        #     ret = spider_service.select_url(md5_page, self.table_name)
        #     if not ret:
        #         spider_service.update_into(md5_page, self.table_name)
        #         yield scrapy.Request(url=c_page, callback=self.parse)
        # # all_page = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[7]/div/div/a/@href').extract()
        # # for c_page in all_page:

    def parse_item(self, response):
        ret = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div')
        for i in range(len(ret)):

            project_name = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[1]/h3/a/text()'.format(i + 1)).extract()[0]
            project_desc = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[1]/p/text()'.format(i + 1)).extract()[0]
            project_process = u''
            if response.url.startswith(u'http://www.zhongchou.com/browse/di'):
                project_process = u'众筹中'
            elif response.url.startswith(u'http://www.zhongchou.com/browse/rd'):
                project_process = u'将要结束'
            elif response.url.startswith(u'http://www.zhongchou.com/browse/re'):
                project_process = u'成功结束'
            rr = Selector(response=response).xpath(
                '//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[2]/div[1]/a/text()'.format(i + 1))
            project_tag = u''
            for k in range(len(rr)):

                tag = Selector(response=response).xpath(
                    '//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[2]/div[1]/a[{}]/text()'.format(i + 1, k + 1)).extract()[0]

                project_tag = project_tag + " " + tag
            project_fundraising = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[2]/div[3]/div[1]/p[1]/text()'.format(i + 1)).extract()[0].split('￥')[1]
            project_support = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[2]/div[3]/div[2]/p[1]/text()'.format(i + 1)).extract()[0]
            fundraising_progress = Selector(response=response).xpath('//*[@id="ng-app"]/body/div[6]/div/div[{}]/div/div[2]/div[3]/div[3]/p[1]/text()'.format(i + 1)).extract()[0]
        # html = response.body
        # all_project = PyQuery(html).find('.ssCardItem')
        # for c_project in all_project:
        #     project_name = PyQuery(c_project).find('.ssCardICText').find('a').attr("title")
        #     project_desc = PyQuery(c_project).find('.ssCardICText').find('p').text()
        #     project_process = u''
        #     if response.url.startswith(u'http://www.zhongchou.com/browse/di'):
        #         project_process = u'众筹中'
        #     elif response.url.startswith(u'http://www.zhongchou.com/browse/rd'):
        #         project_process = u'将要结束'
        #     elif response.url.startswith(u'http://www.zhongchou.com/browse/re'):
        #         project_process = u'成功结束'
        #     tag_list = PyQuery(c_project).find('.siteCardFLabelBox').children('a')
        #     project_tag = u''
        #     for c_tag in tag_list:
        #         project_tag = project_tag + " " + PyQuery(c_tag).text()
        #     c_list = PyQuery(c_project).find('.ftP')
        #     project_fundraising = PyQuery(c_list[0]).text()
        #     project_support = PyQuery(c_list[0]).text()
        #     fundraising_progress = PyQuery(c_list[0]).text()
            item_obj = ZhongchouItem(project_name=project_name, project_desc=project_desc,
                                     project_process=project_process, project_tag=project_tag,
                                     project_fundraising=project_fundraising, project_support=project_support,
                                     fundraising_progress=fundraising_progress)
            yield item_obj

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(url)
        return obj.hexdigest()
