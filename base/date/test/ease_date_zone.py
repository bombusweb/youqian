#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pytz import timezone, utc
import datetime
from calendar import timegm

timestamp=int(time.time())
#时间戳
print timestamp
#日期+时间

now=datetime.datetime.fromtimestamp(timestamp)
print now

tz=timezone('Asia/Shanghai')
now_zone=tz.localize(now, is_dst=None)
print now_zone
  
print now_zone.utctimetuple()

utc_timestamp=timegm(now_zone.utctimetuple()) + now_zone.microsecond / 1000000
print utc_timestamp
