#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re

re_user_agent = re.compile(r'(iPhone|iPod|Android|ios|iPad)')
re_ios_user_agent = re.compile(r'(iPhone|iPod|ios|iPad)')