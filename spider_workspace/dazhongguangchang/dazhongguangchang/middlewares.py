# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class DazhongguangchangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random
from scrapy import signals
# from .settings import IPPOOL
from .dao import db_module
from test_proxy import test_proxy
class MyproxiesSpiderMiddleware(object):
    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        flage = True

        while flage:

            sql = "select ip_port from ip_pool"
            IPPOOL = db_module.execute_getinfo(sql)
            print IPPOOL
            thisip = random.choice(IPPOOL)
            ip_port = thisip[0]
            key = True
            i = 0
            while key:
                i += 1
                obj = test_proxy.TestProxy(ip_port)
                ret = obj.run()
                print ret
                if ret:
                    flage = False
                    key = False
                    print("this is ip:" + ip_port)
                    request.meta["proxy"] = ip_port
                else:
                    if i == 3:
                        sql = "delete from ip_pool where ip_port='{}'".format(ip_port)
                        db_module.execute_into(sql)