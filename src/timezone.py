#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Timezone info
"""

import datetime


class Timezone(datetime.tzinfo):

    def __init__(self, arg):
        super(GMT8, self).__init__()
        self.arg = arg


class GMT8(datetime.tzinfo):
    """docstring for GMT8"""
    def __init__(self, arg):
        super(GMT8, self).__init__()
        self.arg = arg

    def utcoffset(self, dt):
        # 8 hours ahead of GMT
        return timedelta(hours=8)

    def tzname(self, dt):
        return "GMT +8"

    def dst(self, dt):
        return timedelta(0)


class GMT8(datetime.tzinfo):
    """docstring for GMT8"""
    def __init__(self, arg):
        super(GMT8, self).__init__()
        self.arg = arg

    def utcoffset(self, dt):
        # 8 hours ahead of GMT
        return timedelta(hours=8)

    def tzname(self, dt):
        return "GMT +8"

    def dst(self, dt):
        return timedelta(0)
