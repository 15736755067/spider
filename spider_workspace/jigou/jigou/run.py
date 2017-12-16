from scrapy import cmdline
# cmdline.execute("scrapy crawl ji_gou".split())
cmdline.execute("scrapy crawl ji_gou -s JOBDIR=crawls/ji_gou-1".split())