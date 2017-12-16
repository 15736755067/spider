from scrapy import cmdline
import time
while True:
    cmdline.execute("scrapy crawl ip".split())
    time.sleep(120)
# cmdline.execute("scrapy crawl zhi_lian -s JOBDIR=crawls/zhi_lian-1".split())