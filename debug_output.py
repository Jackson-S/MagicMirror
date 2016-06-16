# -*- coding: UTF-8 -*-
"""Displays timestamped module info as well as system info"""

import time
from os import uname
from sys import version as pyver

import pygame

from config.settings import show_debug


def startupinfo():
    """Prints system information to stdout"""
    if show_debug is True:
        try:
            print("OS={}".format(
                uname()[3]))
        except AttributeError:
            pass

        try:
            print("PYGAME={}, BACKEND={}".format(
                pygame.vernum, pygame.display.get_driver()))
        except AttributeError:
            pass

        try:
            print("PYTHON={}".format(
                pyver))
        except AttributeError:
            pass

        try:
            print("VIDEO={}".format(
                pygame.display.Info()))
        except AttributeError:
            pass

        try:
            print("DIRECTX={}".format(
                pygame.dx_version_string))
        except AttributeError:
            pass


def timestamp(activity, priority=0):
    """Prints timestamps of functions"""
    if show_debug is True or priority > 0:
        year, month, day, hour, minute, second = time.localtime()[0:6]
        print("{}/{}/{} {}:{}:{}:{} - {}".format(
            year, month, day, hour, minute, second,
            str(time.time() - int(time.time()))[2:6], activity))
