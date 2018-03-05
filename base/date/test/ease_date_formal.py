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
tz=timezone('Asia/Shanghai')
now=datetime.datetime.fromtimestamp(timestamp,tz)
print now

utc_timestamp=timegm(now.utctimetuple()) + now.microsecond / 1000000
print utc_timestamp
