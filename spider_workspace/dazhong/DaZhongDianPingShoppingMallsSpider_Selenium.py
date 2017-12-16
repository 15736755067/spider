# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions
class SeleniumConf(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 100)

    def getPage(self,url):
        try:
            print 'start to query square...'
            self.driver.get(url)
        except TimeoutException:
            print 'square page(%s) loaded timeout...' % url
            return False
        else:
            return True

    def waitUtil(self, element):
        self.wait.until(EC.presence_of_element_located((By.XPATH, element)))

    def elementsExist(self, driver, xpath_str):
        try:
            elements_list = driver.find_elements_by_xpath(xpath_str)
            return elements_list
        except:
            return False

    def elementExist(self, driver, xpath_str):
        try:
            element = driver.find_element_by_xpath(xpath_str)
            return element
        except:
            return False

    def getElement(self, driver, xpath_str, params):
        element_exist = self.elementExist(driver, xpath_str)
        try:
            if params == 'href':
                return element_exist.get_attribute(params) if element_exist else None
            elif params == 'innerHTML':
                return element_exist.get_attribute(params) if element_exist else None

            else:
                return element_exist.text if element_exist else None
        except selenium.common.exceptions.NoSuchElementException:
            return None
        except selenium.common.exceptions.StaleElementReferenceException:
            return None

    def findElements(self, xpath_str):
        return self.driver.find_elements_by_xpath(xpath_str)

    def findElement(self, xpath_str):
        return self.driver.find_element_by_xpath(xpath_str).text

    def elementClick(self, element):
        element.click()

    def quit(self):
        self.driver.quit()
        print "query over and driver closed..."
