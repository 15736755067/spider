from scrapy import cmdline
# cmdline.execute("scrapy crawl zhong".split())
cmdline.execute("scrapy crawl zhong -s JOBDIR=crawls/zhong-1".split())