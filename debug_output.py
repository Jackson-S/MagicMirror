# -*- coding: UTF-8 -*-

import time
import pygame
from os import uname
from sys import version as pyver
from config.settings import timestamp as show


def startupinfo():
    try:
        print("OS={}".format(
            uname()[3]))
        print("PYGAME={}, BACKEND={}".format(
            pygame.vernum, pygame.display.get_driver()))
        print("PYTHON={}".format(
            pyver))
        print("VIDEO={}".format(
            pygame.display.Info()))
        print("DIRECTX={}".format(
            pygame.dx_version_string))
    except AttributeError:
        pass


def timestamp(activity, priority="low", show_debug=show):
    '''Prints timestamps of functions'''
    if show_debug is True or priority == "high":
        year, month, day, hour, minute, second = time.localtime()[0:6]
        print("{}/{}/{} {}:{}:{} - {}".format(
            year, month, day, hour, minute, second, activity))