#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re


class TestProxy(object):
    def __init__(self, ip):
        self.ip = ip

        self.url = 'http://www.baidu.com'
        self.timeout = 3

        self.regex = re.compile(r'baidu.com')

        # self.run()

    def run(self):

        ret = self.linkWithProxy()
        return ret

    def linkWithProxy(self):
        server = self.ip

        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':server}))
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen(self.url, timeout=self.timeout)
        except:
            print '%s connect failed' % server
            return
        else:
            try:
                str = response.read()

            except:
                print '%s connect failed' % server
                return
            if self.regex.search(str):
                print '%s connect success .......' % server
                print self.ip
                return self.ip


# if __name__ == '__main__':
#     Tp = TestProxy(ip)
#     Tp.run()