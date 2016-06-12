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
from sys import argv
import time
import pygame
import config.settings as settings
from config.translations import modes
from debug_output import timestamp, startupinfo
from modules.bom.bom_weather_module import BOMWeatherModule
from modules.time.time_module import TimeModule
from modules.reddit.reddit_module import RedditModule
from modules.framerate.framerate_module import FramerateModule
from modules.loading.loadingmodule import LoadingModule


def get_display_mode():
    '''returns the desired display mode integer'''
    try:
        mode = argv[1]
    except IndexError:
        return modes[settings.def_disp_mode]
    try:
        return modes[mode]
    except KeyError:
        timestamp("{}".format(translations.disp_err_str.format(mode, settings.def_disp_mode)))
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
    '''UI of the program, loads and draws all modules.'''

    timestamp("Initialising main program...")
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(MOUSE_VISIBLE)
    timestamp("Loading modules...")
    modules = []

    '''To add a new module first add it to the import list at the top
    and then add it to this list using this format:

    timestamp("Loading BOMWeatherModule")
    modules.append(BOMWeatherModule(WIDTH, HEIGHT, COLOUR[2], [OTHER REQUIREMENTS]))

    COLOUR[2] is the foreground colour, and other requirements is anything else
    your module requires from the main loop in order to display correctly.
    Fonts can either be imported here or created in module in the __init__
    function.
    The timestamp isn't needed but it will help with debugging
    if your module causes errors.
    '''

    timestamp("Loading BOMWeatherModule")
    modules.append(BOMWeatherModule(WIDTH, HEIGHT, COLOUR[2]))
    timestamp("Loading RedditModule")
    modules.append(RedditModule(WIDTH, HEIGHT, COLOUR[2], FONT[6], FONT[7]))
    timestamp("Loading TimeModule")
    modules.append(TimeModule(WIDTH, HEIGHT, COLOUR[2], FONT[1]))
    #timestamp("Loading FramerateModule")
    #modules.append(FramerateModule(WIDTH, HEIGHT, COLOUR[2], FONT[3], game_clock))
    timestamp("Completed loading modules.")

    module_display = [None]*len(modules)
    requires_update = False
    while True:
        check_events(pygame.event.get())
        game_clock.tick()
        while requires_update is False:
            for module_no, module in enumerate(modules):
                if module.need_update() is True:
                    module_display[module_no] = module.update()
                    requires_update = True
                    timestamp("Updating {}".format(module), show_debug=False)
                check_events(pygame.event.get())
                # Wait 0.5 seconds before retrying to save power:
                time.sleep(0.5)
        if requires_update is True:
            SCREEN.fill(COLOUR[0])
            for module in module_display:
                for item, item_pos in module:
                    SCREEN.blit(item, item_pos)
            requires_update = False
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

    # Display the loading screen (loading module):
    loading = LoadingModule(WIDTH, HEIGHT)
    loading = loading.update()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(loading[0], loading[1])
    pygame.display.flip()
    del loading

    # Add generic settings:
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
    startupinfo()
    main()
