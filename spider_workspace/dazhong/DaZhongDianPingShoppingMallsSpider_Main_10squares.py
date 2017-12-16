# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import logging

logger = logging.getLogger()
logging.basicConfig(
    filename='dazhongdianping_shoppingmalls.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
)

import time
import calendar
import requests

now = time.localtime()
month_range = calendar.monthrange(now.tm_year, now.tm_mon)[1]
day_end = '%d-%02d-%02d' % (now.tm_year, now.tm_mon, month_range)

import pandas as pd
from DaZhongDianPingShoppingMallsSpider_Requests import RequestsConf
from DaZhongDianPingShoppingMallsSpider_Selenium import SeleniumConf
from DaZhongDianPingShoppingMallsSpider_MySql import MySqlConf
from xpinyin import Pinyin

if __name__ == '__main__':
    gc_dict = {'66847744': '南昌'}
    gc_id_dict = {'上海': '1', '北京': '2', '武汉': '16', '长沙': '344', '合肥': '110', '福州': '14', '西安': '17', '济南': '22',
                  '温州': '101', '深圳': '7', '景洪市': '1908','贵阳':'258','南昌':'134'}
    common_url = "https://www.dianping.com/shop/"
    mysql_conf = MySqlConf()
    ret1 = mysql_conf.select_sql()

    for gc_id, city_name in gc_dict.iteritems():
        sele = SeleniumConf()
        city_id = gc_id_dict[city_name]
        gc_url = common_url + gc_id
        print gc_url
        gc_status = sele.getPage(gc_url)
        if gc_status:
            wait_gc_name_element = "//div[@class='page-main']/div[2]/div[1]/div[2]/h2"
            gc_name = sele.findElement(wait_gc_name_element)
            wait_a_elements = "//div[@class='page-main']/div[@class='mod brand J_brandshops']//div[@class='brand-category']/a"
            sele.waitUtil(wait_a_elements)
            a_elements_list = sele.findElements(wait_a_elements)
            for a_idx, a in enumerate(a_elements_list):
                if a_idx != 0:
                    results_info_list = []
                    sele.elementClick(a)
                    while True:
                        nextpage_exist = sele.elementExist(sele.driver,
                                                           "//*[@id='brand-container']/a[@class='brand-next']")
                        if nextpage_exist:
                            sele.elementClick(nextpage_exist)
                        else:
                            break
                    label = a.get_attribute('innerHTML')
                    print u'业态:', label
                    wait_div_elements = "//*[@id='brand-container']//div[@class='brand-content']/div[@class='mod-body fn-clear' and @status='loaded']/div"
                    sele.waitUtil(wait_div_elements)
                    div_elements = sele.findElements(wait_div_elements)
                    for div in div_elements:
                        store_name = sele.getElement(div, "./div[@class='brand-info']/p[@class='name']", "innerHTML")
                        # store_img = sele.getElement(div, "./div[@class='brand-logo brand-logo-v']/img", "src")
                        store_url = sele.getElement(div, "./a", "href")
                        # if store_img != None:
                        #     try:
                        #         pic = requests.get(store_img, timeout=10)
                        #     except requests.exceptions.ConnectionError:
                        #         print '【错误】当前图片无法下载'
                        #         continue
                        #     string = 'C:\Users\Administrator\Desktop\jpg\\' + store_url[30:] + '.jpg'
                        #     fp = open(string, 'wb')
                        #     fp.write(pic.content)
                        #     fp.close()
                        if store_url:
                            store_id = store_url[30:]

                            store_req = RequestsConf()
                            store_status = store_req.request(store_url, 10)

                            if store_status == 200:
                                store_pagesource = store_req.response_content()

                                total_score = store_req.getElement(store_pagesource,
                                                                   ".//*[@id='basic-info']/div[@class='brief-info']/span[1]/@title")
                                comments_num = store_req.reElement(store_pagesource, ".//*[@id='reviewCount']/text()")
                                avg_price = store_req.reElement(store_pagesource, ".//*[@id='avgPriceTitle']/text()")
                                product_score = store_req.reElement(store_pagesource,
                                                                    ".//*[@id='comment_score']/span[1]/text()")
                                environment_score = store_req.reElement(store_pagesource,
                                                                        ".//*[@id='comment_score']/span[2]/text()")
                                service_score = store_req.reElement(store_pagesource,
                                                                    ".//*[@id='comment_score']/span[3]/text()")
                                address = store_req.getElement(store_pagesource,
                                                               ".//*[@id='basic-info']/div[@class='expand-info address']/span[2]/@title")

                                com_sum_before_url = "https://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?shopId=" + store_id
                                req_before = RequestsConf()
                                before_status = req_before.request(com_sum_before_url, 10)
                                if before_status == 200:
                                    com_sum_before_json = req_before.response_json()
                                    shoptype, power = com_sum_before_json['msg']['shopInfo']['shopType'], \
                                                      com_sum_before_json['msg']['shopInfo']['power']
                                    com_sum_after_url = "https://www.dianping.com/ajax/json/shopDynamic/allReview"
                                    req_after = RequestsConf()
                                    params = {'shopId': store_id, 'cityId': city_id, 'categoryURLName': 'food',
                                              'power': power,
                                              'cityEnName': Pinyin().get_pinyin(city_name.decode("utf-8"), ''),
                                              'shopType': shoptype}
                                    after_status = req_after.request(com_sum_after_url, 10, params)
                                    if after_status == 200:
                                        com_sum_list = req_after.response_json()['summarys']
                                        if com_sum_list:
                                            comment_summary = ':'.join(
                                                [com['summaryString'] + '(' + str(com['summaryCount']) + ')' for com in
                                                 com_sum_list])
                                        else:
                                            comment_summary = None
                                    else:
                                        comment_summary = None
                                else:
                                    comment_summary = None

                                results_info_list.append(
                                    [gc_id, gc_name, store_id, store_name, comment_summary, address,
                                     total_score, product_score, environment_score, service_score, comments_num,
                                     avg_price, label])
                                print gc_id, gc_name, store_id, store_name, comment_summary, address, total_score, product_score, environment_score, service_score, comments_num, avg_price, label
                            else:
                                logger.error(
                                    "store page not exist, status_code => %s or page loaded timeout, load next store!!!" % store_status)
                                continue
                        else:
                            logger.warning("store url not exist, next store url...")
                            continue

                    if results_info_list:
                        mysql_conf.insertMysql(results_info_list)
                else:
                    print '全部pass'
                    pass
        else:
            logger.error("gc(%s) load timeout, next gc..." % gc_url)
            continue
        sele.quit()
