#!/usr/bin/env/python3
# -*- coding: UTF-8 -*-

###########################################################
# Python based magic mirror application, based on pygame  #
# library as well as Reddit and BOM weather data.         #
# Licensed under MIT license.                             #
#                                                         #
#                              (c) Jackson Sommerich 2016 #
###########################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from sys import argv, version as pyver
from os import remove, uname
import time
import pygame
import config.settings as settings
import config.translations as translations
from debug_output import timestamp as timestamp
from modules.weather.weather import fetch_weather_info, parse_weather_info
from modules.time.time_module import TimeModule
from modules.news.news import NewsModule
from modules.framerate.framerate_module import FramerateModule


def truncate(text, title=False, length=100):
    '''truncate(text, title: bool, length: int, suffix: str) -> unicode'''
    if title:
        text = text.title()
    try:
        if len(text) <= length:
            if (text[-1] != "?" or "." or "!" or ":") and not title:
                return u"{}{}".format(text, ".")
            else:
                return u"{}".format(text)
        else:
            return u" ".join(text[:length+1].split(" ")[:-1]) + u"…"
    except UnicodeError:
        return "Error parsing string"


def get_display_mode():
    '''returns the desired display mode integer'''
    try:
        mode = argv[1]
    except IndexError:
        return translations.modes[settings.def_disp_mode]
    try:
        return translations.modes[mode]
    except KeyError:
        timestamp("".format(translations.disp_err_str.format(mode, settings.def_disp_mode)))
        return translations.modes[settings.def_disp_mode]


def check_events(events):
    '''Checks for keyboard events and quits if necessary'''
    for event in events:
        # 2 = pygame.KEYDOWN, 27 = pygame.K_ESCAPE
        if event.type == 2 and event.key == 27:
            timestamp("Quitting...")
            pygame.quit()
            quit()


def main():
    '''main() -> None
    UI of the program, calls all other modules.
    '''

    # Planned features:
    #  - Multiple weather sources
    #  - Automatic on/off based on motion/light sensor

    timestamp("Initialising main program...")
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(MOUSE_VISIBLE)
    modules = [
            NewsModule(SCREEN, COLOUR[2], FONT[6], FONT[7]),
            TimeModule(WIDTH, HEIGHT, COLOUR[2], FONT[1]),
            FramerateModule(WIDTH, HEIGHT, COLOUR[2], FONT[3], game_clock)
            ]
    module_display = [None]*len(modules)
    requires_update = False
    while True:
        game_clock.tick()
        check_events(pygame.event.get())
        for module_no, module in enumerate(modules):
            if module.need_update() is True:
                module_display[module_no] = module.update()
                requires_update = True
                timestamp("Updating {}".format(module), show_debug=False)
        if requires_update is True:
            SCREEN.fill(COLOUR[0])
            for module in module_display:
                for item, item_pos in module:
                    SCREEN.blit(item, item_pos)
            pygame.display.flip()
        check_events(pygame.event.get())


if __name__ == '__main__':
    pygame.init()
    # Mode specifically for my personal setup. Feel free to ignore it/remove it:
    if len(argv) > 1:
        # If running on a raspberry pi use --pi:
        if argv[1] == "--pi":
            RESOLUTION = WIDTH, HEIGHT = (1024, 600)
            SCREEN = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
        # If using any other --option:
        else:
            if settings.autodetect_resolution is True:
                SCREEN = pygame.display.set_mode((0, 0), get_display_mode())
                RESOLUTION = WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
            else:
                RESOLUTION = WIDTH, HEIGHT = settings.resolution
                SCREEN = pygame.display.set_mode(RESOLUTION, get_display_mode())
    # If no arguments are passed:
    else:
        if settings.autodetect_resolution is True:
            SCREEN = pygame.display.set_mode((0, 0), get_display_mode())
            RESOLUTION = WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
        else:
            RESOLUTION = WIDTH, HEIGHT = settings.resolution
            SCREEN = pygame.display.set_mode(RESOLUTION, get_display_mode())
        # Generic settings
    FPS_LIMIT = settings.fps_limit
    MOUSE_VISIBLE = settings.mouse_visible
    TIMESTAMP = settings.timestamp
    SHOW_FPS = settings.display_framerate

    # Initialise the fonts and colours from translations.py:
    if settings.invert_colours:
        COLOUR = [(255, 255, 255), (0, 0, 0), (0, 0, 0)]
    else:
        COLOUR = [(0, 0, 0), (128, 128, 128), (255, 255, 255)]

    FONT = [pygame.font.Font(ttf, int(size*HEIGHT))
            for ttf, size in settings.fonts]
    timestamp("sysinfo")
    main()
