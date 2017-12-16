# -*- coding: utf-8 -*-
import scrapy


class ZhiHuSpider(scrapy.Spider):
    name = 'zhi_hu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
              'Referer': 'https: // www.zhihu.com /',
              }

    def parse(self, response, header=header):
        print response.body
