#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
pool = redis.ConnectionPool(host='192.168.0.5', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
while True:
    rt = r.brpop('job51', 0)
    print rt