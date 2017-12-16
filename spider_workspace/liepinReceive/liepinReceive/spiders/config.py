#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

def create_sleep():
    ret = random.uniform(3, 6)
    time.sleep(ret)

