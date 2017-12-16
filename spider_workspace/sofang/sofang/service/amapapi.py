# -*- coding: utf-8 -*-
from __future__ import division
import torndb
import requests
from amapkey import keys
import re
import pandas as pd
import jieba
from threading import Thread
import amapkey
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

key_index = 0
key = keys[key_index]


def format_address(address):
    if '路' in address:
        address_new = address[0:address.find('路')] + '路'
    elif '道' in address and '街道' not in address:
        address_new = address[0:address.find('道')] + '道'
    elif '街' in address and '街道' not in address:
        address_new = address[0:address.find('街')] + '街'
    elif '街道' in address:
        address_new = address[0:address.find('街道')] + '街道'
    elif '村' in address:
        address_new = address[0:address.find('村')] + '村'
    elif '邨' in address:
        address_new = address[0:address.find('邨')] + '邨'
    elif '镇' in address:
        address_new = address[0:address.find('镇')] + '镇'
    elif '区' in address:
        address_new = address[0:address.find('区')] + '区'
    else:
        address_new = ""
    return address_new


class AMAPApi:
    INFO_CHANGE_KEY = ['IP_QUERY_OVER_LIMIT', 'USER_KEY_RECYCLED', 'INVALID_USER_KEY',
                       'DAILY_QUERY_OVER_LIMIT', 'INVALID_USER_IP', 'USERKEY_PLAT_NOMATCH']
    # , 'UNKNOWN_ERROR'
    def __init__(self):
        self.__key_index = 0
        pass

    def get_places_by_types(self, district_code, types):
        place_lst = list()
        page = 1
        ret = ('-1', place_lst)
        while self.__key_index < len(keys):
            key = keys[self.__key_index]
            ret = self.__get_places_by_types(key, district_code, types, place_lst, page)
            if ret[0] == '-1':
                self.__key_index += 1
                page = ret[1]
            else:
                return (ret[0], place_lst)
        return ret

    def __get_places_by_types(self, key, district_code, types, place_lst, page=1):
        url_f = "http://restapi.amap.com/v3/place/text?key=%s&city=%s&types=%s&page=%s&citylimit=true&extensions=all&offset=20"
        first_cal_count = True
        max_pages = 100
        try:
            for i in range(page, 101):
                if i > max_pages:
                    break
                print 'page:%d' % (i)
                response_json = requests.get(url_f % (key, district_code, types, i)).json()
                info = response_json['info']
                status = response_json['status']
                if first_cal_count and status == '1':
                    count = int(response_json['count'])
                    import math
                    max_pages = int(math.ceil(count / 20))
                    print "pages:%d" % (max_pages)
                    first_cal_count = False
                if status == '1':
                    count = response_json['count']
                    json_pois = response_json['pois']
                    for poi in json_pois:
                        try:
                            kvs = dict()
                            kvs['place_id'] = poi['id'].encode('utf-8')
                            kvs['place_name'] = poi['name'].encode('utf-8')
                            kvs['place_typecode'] = poi['typecode'].encode('utf-8')
                            kvs['adcode'] = poi['adcode'].encode('utf-8')
                            kvs['adname'] = poi['adname'].encode('utf-8')
                            kvs['place_address'] = poi['address'].encode('utf-8')
                            kvs['place_location'] = poi['location'].encode('utf-8')
                            kvs['city_name'] = poi['cityname'].encode('utf-8')
                            kvs['provice_name'] = poi['pname'].encode('utf-8')
                            place_lst.append(kvs)
                        except Exception as e:
                            print e
                else:
                    if info in AMAPApi.INFO_CHANGE_KEY:
                        print key, info
                        return ('-1', i)
                    else:
                        print "%s:%s" % (key, info)
                        return (status, info)
            return ('1', 'ok')
        except Exception as e:
            print e
            return ('0', e.message)

    def get_district_poi(self, district, adcode, subdistrict=True):
        ret = ('0', 'key 用完')
        while self.__key_index < len(keys):
            key = keys[self.__key_index]
            ret = self.__get_district_poi(key, district, adcode, subdistrict)
            if ret[0] == '-1':
                self.__key_index += 1
            else:
                break
        return ret

    def __get_district_poi(self, key, district, adcode, subdistrict=True):
        if subdistrict:
            sd = '1'
        else:
            sd = '0'
        url = "http://restapi.amap.com/v3/config/district?key=%s&keywords=%s&filter=%s&subdistrict=%s" % (
            key, district, adcode, sd)
        try:
            response_json = requests.get(url).json()
            info = response_json['info']
            status = response_json['status']
            if status == '1':
                if subdistrict:
                    json_pois = response_json['districts'][0]['districts']
                else:
                    json_pois = response_json['districts']
                districts = list()
                print len(json_pois)
                for r in json_pois:
                    kvs = dict()
                    kvs['citycode'] = r['citycode']
                    kvs['adcode'] = r['adcode']
                    kvs['name'] = r['name']
                    kvs['level'] = r['level']
                    districts.append(kvs)
                return (status, districts)
            else:

                if info in AMAPApi.INFO_CHANGE_KEY:

                    print key, info
                    return ('-1', list())
                else:
                    print "%s:%s" % (key, info)
                    return (status, info)
        except Exception as e:
            print url
            print e
            return ('0', list())

    def get_place_poi(self, city, keywords, types):
        ret = ('-1', list())
        while self.__key_index < len(keys):
            key = keys[self.__key_index]
            ret = self.__get_place_poi(key, city, keywords, types)
            if ret[0] == '-1':
                self.__key_index += 1
            else:
                break
        return ret

    def __get_place_poi(self, key, city, keywords, types):
        url = "http://restapi.amap.com/v3/place/text?key=%s&city=%s&keywords=%s&types=%s&citylimit=true&extensions=all&offset=20" % (
            key, city, keywords, types)
        try:
            response_json = requests.get(url).json()
            info = response_json['info']
            status = response_json['status']
            if status == '1':
                json_pois = response_json['pois']
                pois = list()
                for poi in json_pois:
                    kvs = dict()
                    # poi = json_pois[0]
                    kvs['place_id'] = poi['id']
                    kvs['place_name'] = poi['name']
                    kvs['place_address'] = poi['address']
                    kvs['place_location'] = poi['location']
                    kvs['place_typecode'] = poi['typecode']
                    if poi.has_key('entr_location'):
                        kvs['place_entr_location'] = poi['entr_location']
                    if poi.has_key('exit_location'):
                        kvs['place_exit_location'] = poi['exit_location']
                    if poi.has_key('business_area'):
                        kvs['place_business_area'] = poi['business_area']
                    if poi.has_key('gridcode'):
                        kvs['place_gridcode'] = poi['gridcode']
                    pois.append(kvs)
                return (status, pois)
            else:

                if info in AMAPApi.INFO_CHANGE_KEY:
                    print key, info
                    return ('-1', list())
                else:
                    print "%s:%s" % (key, info)
                    return (status, list())
        except Exception as e:
            print url
            print e
            return ('0', list())

    def get_geo_poi(self, city, address):
        ret = ('-1', dict())
        while self.__key_index < len(keys):
            key = keys[self.__key_index]
            ret = self.__get_geo_poi(key, city, address)
            if ret[0] == '-1':
                self.__key_index += 1
            else:
                break
        return ret

    def __get_geo_poi(self, key, city, address):
        url = "http://restapi.amap.com/v3/geocode/geo?key=%s&city=%s&address=%s" % (key, city, address)
        try:
            response_json = requests.get(url).json()
            info = response_json['info']
            status = response_json['status']
            if status == '1':
                json_pois = response_json['geocodes']
                kvs = dict()
                if json_pois:
                    poi = json_pois[0]
                    kvs['geo_address'] = poi['formatted_address']
                    kvs['geo_location'] = poi['location']
                    kvs['geo_level'] = poi['level']
                return (status, kvs)
            else:

                if info in AMAPApi.INFO_CHANGE_KEY:
                    print key, info
                    return ('-1', dict())

                else:
                    print "%s:%s" % (key, info)
                    return (status, dict())
        except Exception as e:
            print url
            print e
            return ('0', dict())

def print_geo_poi(poi):
    print poi['geo_level']
    print poi['geo_address']
    print poi['geo_location']

if __name__ == '__main__':
    ret = AMAPApi().get_geo_poi('北京','北京市朝阳区 北京卜蜂莲花青年路店')
    print print_geo_poi(ret[1])
