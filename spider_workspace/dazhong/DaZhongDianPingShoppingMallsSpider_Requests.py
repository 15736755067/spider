# -*- coding: utf-8 -*-

import re
import requests
from lxml import etree
from StringIO import StringIO as SIO
class RequestsConf(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 's_ViewType=10; aburl=1; cy=1; cye=shanghai; _hc.v=c62fe3bd-7577-a859-8fd2-b1d83598fb8d.1494320437; __mta=210171434.1494828661110.1494854962695.1494855005086.4; JSESSIONID=D1D704D69E38412B91C04A1BBDDF4DBC; PHOENIX_ID=0a0168c9-15c13d1b6c0-96f84a',
            'Host': 'www.dianping.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        }
        self.response = None

    def request(self, url, timeout=None, params=None):
        try:
            self.response = requests.get(url, headers=self.headers, params=params, timeout=timeout)
        except Exception, e:
            print '%s, page(%s) timeout, loaded error!!!' % (e, url)
            return False
        else:
            print 'response status: %d, [%s]' % (self.response.status_code, url)
            return self.response.status_code

    def response_json(self):
        return self.response.json()

    def response_content(self):
        content = self.response.content.decode('UTF-8')
        pagesource = etree.parse(SIO(content), etree.HTMLParser())
        return pagesource

    def elementsExist(self, pagesource, xpath_str):
        try:
            elements_list = pagesource.xpath(xpath_str)
            return elements_list
        except:
            return False

    def elementExist(self, pagesource, xpath_str):
        try:
            element = pagesource.xpath(xpath_str)
            return element
        except:
            return False

    def getElement(self, driver, xpath_str):
        element_exist = self.elementExist(driver, xpath_str)
        return element_exist[0] if element_exist else None

    def reElement(self, driver, xpath_str):
        element = self.getElement(driver, xpath_str)
        re_element = re.findall('\d+.\d+|\d+', element) if element else None
        try:
            element = re_element[0]
        except:
            return None
        else:
            return element
