#!/usr/bin/env/python3
# -*- coding: UTF-8 -*-

""" Python based modular magic mirror application,
    design your own modules or use the included ones!

    Program and included modules are licensed under the
    MIT license and are © Jackson Sommerich (2016). This
    excludes existing third party libraries, other third
    party works and third party data services used;
    whose licenses can be found in the LICENSE.md file
    or through the managing body in cases where licenses
    could not be obtained.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

import pygame

import config.settings as settings
from debug_output import timestamp, startupinfo
from modules.bom.bom_weather_module import BOMWeatherModule
from modules.loading.loadingmodule import LoadingModule
from modules.reddit.reddit_module import RedditModule
from modules.time.time_module import TimeModule
from modules.picture.picturemodule import PictureModule


# from modules.framerate.framerate_module import FramerateModule

#############################################################################
# Tutorial module below, uncomment and follow instructions in main() to try #
#############################################################################
# from modules.sample.samplemodule import SampleModule


def get_display_mode():
    """returns the desired display mode for the display object"""
    # Parse all display arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen",
                        action="store_true",
                        default=False)
    info = pygame.display.Info()
    parser.add_argument("-r", "--resolution",
                        action="store",
                        default=(info.current_w, info.current_h),
                        help="width height",
                        nargs=2,
                        type=int)
    if parser.parse_args().fullscreen is True:
        mode = pygame.FULLSCREEN
    else:
        mode = 0
    res = parser.parse_args().resolution
    pygame.display.set_caption("Magic Mirror")
    return res[0], res[1], mode


def check_events(events):
    """Checks for keyboard events and quits if necessary"""
    for event in events:
        # 2 = pygame.KEYDOWN, 27 = pygame.K_ESCAPE
        if event.type == 2 and event.key == 27:
            timestamp("Quitting...")
            pygame.quit()
            quit()


def main():
    """UI of the program, loads and draws all modules."""

    timestamp("Initialising main program...")
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(settings.mouse_visible)
    timestamp("Loading modules...")
    modules = []

    ###########################################################################
    # '''To add a new module first add it to the import list at the top       #
    # and then add it to this list using this format:                         #
    #                                                                         #
    # timestamp("Loading SampleModule")                                       #
    # modules.append(SampleModule(WIDTH, HEIGHT, COLOUR[2], [OTHER]))         #
    #                                                                         #
    # COLOUR[2] is the foreground colour, and other is anything else          #
    # your module requires from the main loop in order to display correctly.  #
    # Fonts can either be imported here or created in module in the __init__  #
    # function.                                                               #
    # The timestamp isn't needed but it will help with debugging              #
    # if your module causes errors.                                           #
    ###########################################################################

    timestamp("Loading PictureModule")
    modules.append(PictureModule(WIDTH, HEIGHT))
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

    module_display = [None] * len(modules)
    requires_update = False
    waited = False
    while True:
        check_events(pygame.event.get())
        game_clock.tick()
        while True:
            for module_no, module in enumerate(modules):
                if module.need_update() is True:
                    module_display[module_no] = module.update()
                    requires_update = True
                check_events(pygame.event.get())
            if requires_update is True:
                # Wait 0.5 seconds to see if we can group
                # any screen updates to save power:
                if waited is False:
                    pygame.time.wait(500)
                    waited = True
                else:
                    waited = False
                    break
            else:
                pygame.time.wait(1)
        if requires_update is True:
            timestamp("Commencing screen update...")
            SCREEN.fill(COLOUR[0])
            for module in module_display:
                for item, item_pos in module:
                    SCREEN.blit(item, item_pos)
            requires_update = False
            pygame.display.flip()
            timestamp("Completed screen update...\n")
        check_events(pygame.event.get())


if __name__ == '__main__':
    pygame.init()
    WIDTH, HEIGHT, MODE = get_display_mode()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), MODE)

    # Initialise the fonts and colours from settings.py:
    COLOUR = [
        settings.colour[0],
        settings.colour[1],
        settings.colour[2]
    ]
    FONT = [pygame.font.Font(ttf, int(pt * HEIGHT)) for ttf, pt in settings.fonts]

    # Display the loading screen (loading module):
    LOADING = LoadingModule(WIDTH, HEIGHT, COLOUR[2], FONT[0])
    LOADING_DISP = LOADING.update()
    SCREEN.fill(COLOUR[0])
    SCREEN.blit(LOADING_DISP[0], LOADING_DISP[1])
    pygame.display.flip()
    # Delete the module as it is only displayed once
    del LOADING, LOADING_DISP

    startupinfo()
    main()
