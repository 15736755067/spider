#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
header= {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.8",
"Connection":"keep-alive",
"Cookie":"_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=15f03e3b6fcc8-0f390fa30ad0e1-3a3e5f04-13c680-15f03e3b6fdc8; _lxsdk=15f03e3b6fcc8-0f390fa30ad0e1-3a3e5f04-13c680-15f03e3b6fdc8; _hc.v=5946fe73-7e41-d1df-dbcb-dc63625abc07.1507598776; s_ViewType=10; JSESSIONID=13B0E60DF876AC5D470042A08170E88D; aburl=1; cy=145; cye=zibo; __mta=253006390.1507602899934.1507616487489.1507616696959.18; _lxsdk_s=15f04c9902a-707-cde-90c%7C%7C184",
"Host":"www.dianping.com",
"Upgrade-Insecure-Requests":1,
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

url = 'http://www.dianping.com/shop/81084633'
ret = requests.get(url=url,headers=header)
print ret.text

