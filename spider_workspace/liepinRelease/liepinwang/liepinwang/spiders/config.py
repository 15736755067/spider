#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

def create_sleep():
    ret = random.uniform(10, 15)
    time.sleep(ret)
    print ret
