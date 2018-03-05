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

utc_timestamp=timegm(now.utctimetuple()) + now.microsecond / 1000000
print utc_timestamp
