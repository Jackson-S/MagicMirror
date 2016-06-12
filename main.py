#!/usr/bin/env/python3
# -*- coding: UTF-8 -*-

''' Python based magic mirror application, based on pygame
    library as well as Reddit and BOM weather data.
    Licensed under MIT license.

                            (c) Jackson Sommerich 2016
'''


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
# from modules.framerate.framerate_module import FramerateModule
from modules.loading.loadingmodule import LoadingModule

#############################################################################
# Tutorial module below, uncomment and follow instructions in main() to try #
#############################################################################
# from modules.sample.samplemodule import SampleModule


def get_display_mode():
    '''returns the desired display mode integer'''
    try:
        mode = argv[1]
    except IndexError:
        return modes[settings.def_disp_mode]
    try:
        return modes[mode]
    except KeyError:
        timestamp("Display mode error. Using default")
        return modes[settings.def_disp_mode]


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
    pygame.mouse.set_visible(settings.mouse_visible)
    timestamp("Loading modules...")
    modules = []

    ############################################################################
    # '''To add a new module first add it to the import list at the top        #
    # and then add it to this list using this format:                          #
    #                                                                          #
    # timestamp("Loading SampleModule")                                        #
    # modules.append(SampleModule(WIDTH, HEIGHT, COLOUR[2], [OTHER]))          #
    #                                                                          #
    # COLOUR[2] is the foreground colour, and other is anything else           #
    # your module requires from the main loop in order to display correctly.   #
    # Fonts can either be imported here or created in module in the __init__   #
    # function.                                                                #
    # The timestamp isn't needed but it will help with debugging               #
    # if your module causes errors.                                            #
    ############################################################################

    timestamp("Loading BOMWeatherModule")
    modules.append(BOMWeatherModule(WIDTH, HEIGHT, COLOUR[2]))
    timestamp("Loading RedditModule")
    modules.append(RedditModule(WIDTH, HEIGHT, COLOUR[2], (FONT[6], FONT[7])))
    timestamp("Loading TimeModule")
    modules.append(TimeModule(WIDTH, HEIGHT, COLOUR[2], FONT[1]))
######
    ##############################################################
    # Enable this module to use the "hello world" sample module. #
    ##############################################################
    # timestamp("Loading SampleModule")
    # modules.append(SampleModule(WIDTH, HEIGHT, COLOUR[2]))
######
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
                # Wait 1 second before retrying to save power:
                pygame.time.wait(1000)
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
    # If display arguments are passed:
    if len(argv) > 1:
        if settings.autodetect_resolution is True and argv[1] != "--window":
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
    LOADING = LoadingModule(WIDTH, HEIGHT)
    LOADING_DISP = LOADING.update()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(LOADING_DISP[0], LOADING_DISP[1])
    pygame.display.flip()
    # Delete the module as it is only displayed once
    del LOADING, LOADING_DISP

    # Initialise the fonts and colours from settings.py:
    COLOUR = [
        settings.colour[0],
        settings.colour[1],
        settings.colour[2]
        ]
    FONT = [pygame.font.Font(ttf, int(pt*HEIGHT))for ttf, pt in settings.fonts]
    startupinfo()
    main()
