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

from config.settings import fonts, colour, mouse_visible
from debug_output import timestamp, startupinfo

from modules.loading.loadingmodule import LoadingModule
from modules.picture.picturemodule import PictureModule
from modules.bom.bom_weather_module import BOMWeatherModule
from modules.reddit.reddit_module import RedditModule
from modules.time.time_module import TimeModule

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


def cleanquit():
    """Quits pygame correctly"""
    timestamp("Quitting.")
    pygame.quit()
    quit()


def check_events():
    """Checks for keyboard events and quits if necessary"""
    for event in pygame.event.get():
        # 2 = pygame.KEYDOWN, 27 = pygame.K_ESCAPE, 12 = window x button.
        if (event.type == 2 and event.key == 27) or (event.type == 12):
            cleanquit()


def loadingscreen(screen):
    """Displays the loading screen"""
    module = LoadingModule()
    text, textpos = module.update()
    screen.fill(COLOUR[0])
    screen.blit(text, textpos)
    pygame.display.flip()


def main(screen):
    """UI of the program, loads and draws all modules."""

    timestamp("Initialising main program...")
    startupinfo()
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(mouse_visible)

    ###########################################################################
    # '''To add a new module first add it to the import list at the top       #
    # and then add it to this list using this format:                         #
    #     SampleModule(WIDTH, HEIGHT, COLOUR[2])                              #
    #                                                                         #
    # COLOUR[2] is the foreground colour, add to the end anything else        #
    # your module requires from the main loop in order to display correctly.  #
    # Fonts can either be imported here or created in module in the __init__  #
    # function.                                                               #
    # The timestamp isn't needed but it will help with debugging              #
    # if your module causes errors.                                           #
    ###########################################################################

    timestamp("Loading modules...")
    modules = [PictureModule(),
               BOMWeatherModule(),
               RedditModule(),
               TimeModule(),
               # SampleModule()
               ]
    timestamp("Completed loading modules.")

    module_display = [None] * len(modules)
    requires_update = False
    while True:
        game_clock.tick()
        while True:
            while requires_update is False:
                for module_no, module in enumerate(modules):
                    if module.need_update() is True:
                        module_display[module_no] = module.update()
                        requires_update = True
                check_events()
                pygame.time.wait(200)
            timestamp("Commencing screen update...")
            screen.fill(COLOUR[0])
            for module in module_display:
                for item, item_pos in module:
                    screen.blit(item, item_pos)
            pygame.display.flip()
            requires_update = False
            timestamp("Completed screen update...\n")


if __name__ == '__main__':
    pygame.init()
    # Fetches passed arguments and gets the current screen size:
    WIDTH, HEIGHT, MODE = get_display_mode()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), MODE)
    # Initialise the fonts and colours from settings.py:
    COLOUR = [colour[0], colour[1], colour[2]]
    FONT = [pygame.font.Font(ttf, int(pt * HEIGHT)) for ttf, pt in fonts]
    # Display the loading screen (LoadingModule):
    loadingscreen(SCREEN)
    # Redirect keyboard interrupt to standard close procedure. Suppresses
    # associated warnings:
    try:
        main(SCREEN)
    except KeyboardInterrupt:
        cleanquit()
