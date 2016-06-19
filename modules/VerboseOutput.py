# -*- coding: UTF-8 -*-
"""Displays timestamped module info as well as system info"""

import time
from settings import show_debug


def timestamp(activity, priority=0):
    """Prints timestamps of functions"""
    if show_debug is True or priority > 0:
        year, month, day, hour, minute, second = time.localtime()[0:6]
        print("{}/{}/{} {}:{}:{}:{} - {}".format(
            year, month, day, hour, minute, second,
            str(time.time() - int(time.time()))[2:6], activity))
